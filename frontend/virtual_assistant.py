import streamlit as st
import requests

API_URL = "http://127.0.0.1:5000/chat"

st.title("TBO AI Chatbot")
st.write("Ask me about Medical Tourism, MICE, or Destination Weddings!")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("You:", "")

if st.button("Send"):
    if user_input:
        response = requests.post(API_URL, json={"message": user_input}).json()
        bot_response = response.get("response", "I'm not sure about that.")
        
        st.session_state.chat_history.append(f"You: {user_input}")
        st.session_state.chat_history.append(f"Bot: {bot_response}")

        user_input = ""

for chat in st.session_state.chat_history:
    st.text(chat)