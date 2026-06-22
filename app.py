import streamlit as st
from rag import get_rag_response
from utils import save_orders

# ---------------------------------------------------------
# 1. Custom CSS Styling (Dark Theme with Red Accent)
# ---------------------------------------------------------
with open("style.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
# ---------------------------------------------------------
# 2. Initialize Session States
# ---------------------------------------------------------
if "order" not in st.session_state:
    st.session_state.order = {
        "order_id": "12345",
        "name": "Ali",
        "address": "123 Main St",
        "status": "Pending"
    }

if "step" not in st.session_state:
    st.session_state.step = "default"

# Renamed to chat_history to bypass previous tuple storage errors completely
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------------------------------------------------
# 3. Process Initial Welcome Hook Message
# ---------------------------------------------------------
if len(st.session_state.chat_history) == 0:
    order = st.session_state.order

    welcome = f"""
📦 **ORDER VERIFICATION SYSTEM**

Hello {order['name']} 👋

Order ID: <span style='color: #E63946; font-weight: bold;'>{order['order_id']}</span> | Current Address: <span style='color: #E63946; font-weight: bold;'>{order['address']}</span> | Status: <span style='color: #E63946; font-weight: bold;'>{order['status']}</span>

Please choose:
- Confirm Order
- Change Address
- Cancel Order
- Ask Question
"""
    st.session_state.chat_history.append({"role": "assistant", "content": welcome})

# ---------------------------------------------------------
# 4. Main Streamlit Layout Rendering
# ---------------------------------------------------------
st.title("SwiftDeliver Logistics")

# Dynamic Alert Status Banner
status = st.session_state.order["status"]
if status == "Pending":
    st.error("🔴 Pending Verification")
elif status == "Verified":
    st.success("🟢 Order Verified")
elif status == "Cancelled":
    st.error("🔴 Order Cancelled")
elif status == "Updated":
    st.info("🔵 Address Updated")

# Render Sidebar Live JSON Data Window
st.sidebar.write("### Current Order Status")
st.sidebar.json(st.session_state.order)

# Draw Chat Screen Interface History
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)

# ---------------------------------------------------------
# 5. Input Stream Process
# ---------------------------------------------------------
user_input = st.chat_input("How can I help you with your order?")


# 1. Helper function for your precise Command Router Intent Classifier
def classify_intent(text):
    text = text.lower().strip()

    # Precise array matches prevent accidental keyword triggers from RAG questions
    if text in ["confirm", "confirm order", "verify", "verify order"]:
        return "confirm"
    if text in ["cancel", "cancel order"]:
        return "cancel"
    if text in ["change address", "update address", "edit address", "change my address"]:
        return "change_address"

    return "question"


if user_input:
    current_query = user_input

    # Append user question instantly to the state history
    st.session_state.chat_history.append({"role": "user", "content": current_query})
    with st.chat_message("user"):
        st.markdown(current_query)

    intent = classify_intent(current_query)
    current_status = st.session_state.order["status"]

    # --- STEP 2: Active Confirmation Stage ---
    if st.session_state.step == "confirm_address":
        confirmation_text = current_query.lower().strip()

        if confirmation_text in ["yes", "confirm", "correct", "y"]:
            st.session_state.order["address"] = st.session_state.pending_address
            st.session_state.order["status"] = "Updated"
            save_orders(st.session_state.order)

            response = f"✅ **Address Updated successfully!** Your new delivery destination is now set to: <span style='color: #E63946; font-weight: bold;'>{st.session_state.order['address']}</span>."
            st.session_state.step = "default"

        elif confirmation_text in ["no", "cancel", "n"]:
            response = "❌ Address update canceled. Kept your original address. How else can I help you?"
            st.session_state.step = "default"

        else:
            response = f"Please confirm with a **Yes** or **No**: Do you want to change your address to `{st.session_state.pending_address}`?"

        st.session_state.chat_history.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response, unsafe_allow_html=True)

    # --- STEP 1: Intercept the raw input address string ---
    elif st.session_state.step == "change_address":
        st.session_state.pending_address = current_query
        st.session_state.step = "confirm_address"

        response = f"You entered: `{current_query}`. Is this correct? Please type **Yes** to confirm or **No** to cancel."

        st.session_state.chat_history.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response, unsafe_allow_html=True)

    # --- DEFAULT COMMAND ROUTER FLOW ---
    else:
        # Guardrail check: Block actions if the order state is already finalized
        if intent in ["confirm", "cancel", "change_address"] and current_status in ["Verified", "Cancelled"]:
            if current_status == "Verified":
                response = "🔒 This order has already been verified. Further modifications are locked."
            else:
                response = "🔒 This order has already been cancelled. No changes can be made."

        else:
            # Process clean un-mutated states safely
            if intent == "confirm":
                st.session_state.order["status"] = "Verified"
                save_orders(st.session_state.order)
                response = "Your order has been verified successfully!"

            elif intent == "cancel":
                st.session_state.order["status"] = "Cancelled"
                save_orders(st.session_state.order)
                response = "Your order has been cancelled."

            elif intent == "change_address":
                st.session_state.step = "change_address"
                response = "Sure, I can help you update your address. Please type your **new shipping address** below 👇"

            else:
                # Regular informational questions fallback safely to standard RAG pipeline
                response = get_rag_response(current_query, st.session_state.order)

        st.session_state.chat_history.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response, unsafe_allow_html=True)

    st.rerun()

# ---------------------------------------------------------
# 6. Sidebar Demo Panel Details
# ---------------------------------------------------------
st.sidebar.divider()
st.sidebar.subheader("🧪 Demo Instructions")
st.sidebar.write("""
1. Type: **Confirm** → verifies order  
2. Type: **Change Address** → update address  
3. Type: **Cancel** → cancels order  
4. Ask: **delivery time / return policy** → uses AI + RAG
""")