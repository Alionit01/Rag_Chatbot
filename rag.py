import faiss
import numpy as np
import streamlit as st
from sentence_transformers import SentenceTransformer
from config import client, GROQ_MODEL, KB_FILE


# -------------------------------------------------------------
# Cached initialization to avoid reloading models on every click
# -------------------------------------------------------------
@st.cache_resource
def initialize_vector_db():
    """
    Loads the embedding model and builds the FAISS index once.
    """
    # 1. Load model
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

    # 2. Read Knowledge base
    try:
        with open(KB_FILE, "r", encoding="utf-8") as f:
            text = f.read()
        chunks = text.split("\n\n")
        kb_chunks = [c.strip() for c in chunks if c.strip()]
    except FileNotFoundError:
        kb_chunks = ["Error: knowledge_base.txt file missing."]

    # 3. Build FAISS index
    embeddings = embedding_model.encode(kb_chunks)
    dimension = embeddings.shape[1]
    faiss_index = faiss.IndexFlatL2(dimension)
    faiss_index.add(np.array(embeddings))

    return embedding_model, faiss_index, kb_chunks


# Single execution invocation context
model, index, kb_chunks = initialize_vector_db()


# -----------------------
# Search function
# -----------------------
def search_kb(query, top_k=1):
    """
    Finds the most semantically relevant chunk from the text database using vector math.
    """
    query_embedding = model.encode([query])
    distances, indices = index.search(np.array(query_embedding), top_k)
    results = [kb_chunks[i] for i in indices[0]]
    return results


# -----------------------
# Groq Inference Pipeline
# -----------------------
def get_rag_response(user_input, order):
    """
    Combines FAISS context and Order State to query Groq LLM.
    """
    # 1. Retrieve knowledge base context using vector search
    context = search_kb(user_input, top_k=1)
    context_text = "\n".join(context)

    # 2. Build the system payload prompt
    prompt = f"""
You are a customer support AI for SwiftDeliver Logistics.

You must answer using company policies when available.

ORDER DETAILS:
- Order ID: {order['order_id']}
- Name: {order['name']}
- Address: {order['address']}
- Status: {order['status']}

KNOWLEDGE BASE:
{context_text}

USER QUESTION:
{user_input}

INSTRUCTIONS:
- Use knowledge base when answering
- Be short and clear
- Help with order + delivery questions
"""

    # 3. Request inference response from Groq
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful order assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content