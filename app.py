# import dependencies
import streamlit as st
from rag_llm import RAG_LLM

st.title("Self-Help Chatbot")

chatbot = RAG_LLM()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

query = st.chat_input("Ask away!")

if query:
    st.chat_message("user").markdown(query)
    st.session_state.messages.append({"role": "user", "content":query})
    response = chatbot.ask(query)
    st.chat_message('assistant').markdown(response)
    st.session_state.messages.append({"role": "assistant", "content":response})