import streamlit as st
import requests

st.set_page_config(page_title="Huawei Mate40 Pro User Manual Chatbot", page_icon="📦", layout="centered")

st.title("📱Huawei Mate40 Pro User Manual Chatbot Demo")

API_URL = "https://manual-4uot.onrender.com/query"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input box
user_input = st.chat_input("Ask a question about your product manual...")
if user_input:
    # Show user message
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Send query to FastAPI backend
    try:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                res = requests.post(API_URL, json={"query": user_input})
                answer = res.json().get("answer", "⚠️ No answer returned.")
                st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
    except Exception as e:
        st.error(f"Request failed: {e}")
