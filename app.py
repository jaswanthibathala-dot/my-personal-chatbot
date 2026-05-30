import streamlit as st
from google import genai
import time

# --- GEMINI API CONFIGURATION ---
# Ikkada mee API key ni paste cheyandi
API_KEY = "AQ.Ab8RN6LNlVK3tzqYiAiG7SwI0au4tqTfp-G0PQoQ0-SEFR_cvQ"

# Client initialize cheyadanki
if "client" not in st.session_state:
    st.session_state.client = genai.Client(api_key=API_KEY)

# App UI Settings
st.set_page_config(page_title="My Personal AI", page_icon="🤖", layout="centered")
st.title("🤖 My Personal Chatbot")
st.write("Welcome! Gemini backend thoti idi mee sontha smart chatbot.")

# Memory create cheskodaniki (Chat history)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Patha messages ni screen meeda chupinchadaniki
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input box
if prompt := st.chat_input("Adagandi, nenu cheptha..."):
    
    # User message screen meeda display chey
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Bot response call
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Gemini API ki input pampinchadam
            response = st.session_state.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            bot_reply = response.text
            
            # ChatGPT laga typing effect ravalante
            for chunk in bot_reply.split(' '):
                full_response += chunk + " "
                time.sleep(0.02)
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
            
        except Exception as e:
            full_response = f"⚠️ Error: API Key correct ga pettaro ledo check cheyandi. {str(e)}"
            message_placeholder.markdown(full_response)
        
    # Bot response memory lo store chey
    st.session_state.messages.append({"role": "assistant", "content": full_response})
