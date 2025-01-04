import streamlit as st
from chatbot import perform_task, get_intent  # Import your chatbot functions

def main():
    st.title("Chatbot Application")
    st.write("Welcome to the Chatbot application. Ask me anything!")

    user_input = st.text_input("You: ", "")

    if user_input:
        intent = get_intent(user_input)
        response = perform_task(intent, user_input)
        st.write("Chatbot: ", response)

if __name__ == "__main__":
    main()
