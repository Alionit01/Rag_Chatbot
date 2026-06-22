# RAG AI Order Verification Assistant
<img width="841" height="806" alt="image" src="https://github.com/user-attachments/assets/28185a4f-fa97-4327-b39c-76f662de9cc9" />

An AI-powered order verification system designed to reduce failed deliveries, incorrect addresses, and unconfirmed orders.

The project combines a rule-based order management system with Retrieval-Augmented Generation (RAG) to create a customer support assistant that can both manage orders and answer company policy questions.

## Problem Statement

Many logistics and e-commerce businesses lose money due to:

* Fake orders
* Incorrect delivery addresses
* Unconfirmed customer information
* Repeated delivery failures

Traditional customer support systems require human intervention for simple verification tasks, increasing operational costs and delays.

## Solution

SwiftDeliver AI Order Verification Assistant automates the order verification process by allowing customers to:

* Confirm orders before dispatch
* Update delivery addresses
* Cancel orders
* Ask questions about delivery policies
* Receive AI-generated responses based on company knowledge

The system uses a hybrid architecture where business-critical actions are handled by predefined rules while customer questions are answered using a RAG pipeline and a Large Language Model.

## Key Features

* AI-powered customer support
* Order verification workflow
* Address update confirmation process
* Order cancellation management
* RAG-based policy retrieval
* Semantic search using vector embeddings
* Real-time chat interface
* Persistent order storage

## Demo Workflow

1. Customer opens the chatbot.
2. Customer confirms, updates, or cancels an order.
3. Order information is updated and stored.
4. Customer can ask policy-related questions.
5. The system retrieves relevant company information.
6. Groq LLM generates a context-aware response.

## Technology Stack

### Frontend

* Streamlit

### Backend

* Python

### AI & RAG

* Groq API
* Llama Model
* Sentence Transformers
* FAISS

### Storage

* JSON

## Project Architecture

User → Streamlit UI → Intent Router

Order Commands → Business Logic → JSON Storage

Customer Questions → RAG Retrieval → Groq LLM → Response

## Project Structure

```text
order_bot/
│
├── app.py
├── config.py
├── rag.py
├── utils.py
├── orders.json
├── knowledge_base.txt
├── requirements.txt
└── README.md
```

### File Descriptions

| File               | Purpose                                               |
| ------------------ | ----------------------------------------------------- |
| app.py             | Main Streamlit application and chatbot interface      |
| config.py          | Groq API configuration                                |
| rag.py             | RAG pipeline, embeddings, and FAISS retrieval         |
| utils.py           | Helper functions for loading and saving orders        |
| orders.json        | Stores customer order data                            |
| knowledge_base.txt | Company policies and business information used by RAG |
| requirements.txt   | Project dependencies                                  |

---

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd order_bot
```

### 2. Create a Virtual Environment (Recommended)

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/macOS:

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If a requirements file is not available, install manually:

```bash
pip install streamlit
pip install groq
pip install sentence-transformers
pip install faiss-cpu
pip install numpy
```

---

## Groq API Setup

Create a Groq API key from:

https://console.groq.com/keys

Open `config.py` and replace:

```python
GROQ_API_KEY = "YOUR_GROQ_API_KEY"
```

with your actual API key.

Example:

```python
GROQ_API_KEY = "gsk_xxxxxxxxxxxxxxxxx"
```

---

## Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

After launching, Streamlit will provide a local URL similar to:

```text
http://localhost:8501
```

Open the URL in your browser.

---

## Sample Commands

Try the following commands inside the chatbot:

### Order Management

```text
confirm order
```

```text
cancel order
```

```text
change address
```

### Policy Questions

```text
What is the delivery time?
```

```text
Can I change my address after shipment?
```

```text
What is your return policy?
```

```text
Do you offer Cash on Delivery?
```

---

## Knowledge Base

The chatbot uses `knowledge_base.txt` as its company knowledge source.

You can customize the business information by editing this file.

Examples include:

* Delivery policies
* Return policies
* Address change policies
* Fraud prevention rules
* Customer support information

After updating the knowledge base, restart the application to rebuild the retrieval index.

## How the RAG Pipeline Works

The project uses a Retrieval-Augmented Generation (RAG) architecture to provide accurate, context-aware responses.

### Step 1: Knowledge Base Loading

Company policies and business information are stored in:

```text
knowledge_base.txt
```

Examples include:

* Delivery policies
* Cancellation policies
* Address update rules
* Return and refund information

---

### Step 2: Text Chunking

The knowledge base is split into smaller chunks so that relevant information can be retrieved efficiently.

---

### Step 3: Embedding Generation

The system uses the following embedding model:

```text
all-MiniLM-L6-v2
```

Each knowledge chunk is converted into a numerical vector representation.

---

### Step 4: Vector Storage

Embeddings are stored in a FAISS vector index.

This enables semantic search instead of simple keyword matching.

---

### Step 5: Retrieval

When a customer asks a question:

```text
Can I change my address after shipment?
```

The question is converted into an embedding and compared against all stored vectors.

The most relevant company policy is retrieved.

---

### Step 6: Response Generation

The retrieved context is sent to the Groq-hosted LLM.

The model generates a response using the retrieved company information rather than relying only on its training data.

---

## Order Verification Workflow

The system separates business actions from AI-generated responses.

### Order Actions

Business-critical operations are handled through predefined rules:

* Confirm Order
* Cancel Order
* Update Address

These actions directly modify order data stored in:

```text
orders.json
```

### Customer Questions

General questions are handled through:

```text
User Question
      ↓
RAG Retrieval
      ↓
Groq LLM
      ↓
Response
```

This prevents AI hallucinations from affecting customer orders.

---

## State Management

The chatbot uses a simple state machine for address updates.

```text
default
   ↓
change_address
   ↓
confirm_address
   ↓
default
```

Example:

```text
User: Change Address
Bot: Enter new address

User: Block 7 Karachi
Bot: Is this address correct?

User: Yes
Bot: Address updated successfully
```

---

## Why This Architecture?

This project follows a hybrid approach:

```text
Rule-Based Logic
        +
Retrieval-Augmented Generation
        +
Large Language Model
```

### Benefits

* Reliable order management
* Reduced AI hallucinations
* Context-aware responses
* Easy to maintain
* Easy to extend

---

## Future Improvements

Potential enhancements include:

* WhatsApp Business integration
* Admin dashboard
* Customer authentication
* Database integration (PostgreSQL/MySQL)
* Order tracking APIs
* Multi-language support
* Risk scoring for suspicious orders
* Human agent escalation

---

## Screenshots

Main chatbot interface
<img width="841" height="806" alt="image" src="https://github.com/user-attachments/assets/3f1226b4-c81c-43fc-a755-b787a54579fe" />
Order confirmation workflow
<img width="920" height="822" alt="image" src="https://github.com/user-attachments/assets/976c3540-994a-4c66-a71a-14840498e705" />
Address update workflow
<img width="822" height="785" alt="image" src="https://github.com/user-attachments/assets/e004253b-c3bf-4418-b025-5af83bcc632c" />
RAG-based question answering
<img width="822" height="733" alt="image" src="https://github.com/user-attachments/assets/fd2f32c2-a264-4adb-946f-6ca37b2b81be" />

Example:

```text
README Images/
├── chatbot.png
├── confirm-order.png
├── update-address.png
└── rag-demo.png
```

---

## Learning Outcomes

Through this project, the following concepts were implemented:

* Retrieval-Augmented Generation (RAG)
* Vector Databases
* Embeddings
* Semantic Search
* LLM Integration
* State Management
* Streamlit Development
* API Integration
* Business Logic Design

---

## Author

Developed as an academic AI project demonstrating the practical application of:

by Ali ur Rehman

---

## License

This project is intended for educational and demonstration purposes.

---

## Conclusion

SwiftDeliver AI Order Verification Assistant demonstrates how modern AI systems can be combined with traditional business logic to create practical, reliable customer support solutions.

By integrating semantic retrieval, vector search, and LLM-powered responses, the system provides accurate policy-based assistance while maintaining strict control over business-critical order operations.

This hybrid architecture makes the solution both intelligent and dependable, reflecting real-world design principles used in modern AI applications.
