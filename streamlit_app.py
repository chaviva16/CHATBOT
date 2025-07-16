import streamlit as st
from intent_detector import get_intent
from task_handler import perform_task  
# ------------------ STREAMLIT UI ------------------ #
st.set_page_config(page_title="Smart Chat Companion", page_icon="🧠")
st.title("🧠 Smart Chat Companion")
st.caption("Ask me anything: weather, date, jokes, conversions & more!")

# Initialize chat history
if "chat" not in st.session_state:
    st.session_state.chat = []

# User input
user_input = st.text_input("Type your message here 👇")

if user_input:
    intent = get_intent(user_input)
    bot_response = perform_task(intent, user_input)

    # Store chat
    st.session_state.chat.append(("You", user_input))
    st.session_state.chat.append(("Bot", bot_response))

# Display chat history
for speaker, message in st.session_state.chat:
    st.markdown(f"**{speaker}**: {message}")
