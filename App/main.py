import streamlit as st
import os
from faq import faq_chain
from router import router
from sql import sql_chain

# Page Config
st.set_page_config(page_title="E-commerce Bot")
st.title("E-commerce Bot")


def ask(query):
    try:
        # Determine intent
        route_choice = router(query)
        route = route_choice.name if route_choice else None

        if route == 'faq':
            return faq_chain(query)
        elif route == 'sql':
            return sql_chain(query)
        else:
            # Default fallback
            return faq_chain(query)
    except Exception as e:
        return f"Error: {e}"


# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

# Capture Input
query = st.chat_input("How can I help you?")

if query:
    # 1. Show User Message
    with st.chat_message("user"):
        st.markdown(query)
    st.session_state.messages.append({"role": "user", "content": query})

    # 2. Generate and Show Response
    response = ask(query)

    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})