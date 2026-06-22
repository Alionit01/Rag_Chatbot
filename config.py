import streamlit as st
from groq import Groq

# Safely initialize the Groq Client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Model configurations
GROQ_MODEL = "llama-3.3-70b-versatile"

# File paths
ORDERS_FILE = "orders.json"
KB_FILE = "knowledge_base.txt"