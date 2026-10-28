import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from core.agent import sales_agent_app

st.set_page_config(
    page_title="Nova | AI Sales Assistant",
    page_icon="💼",
    layout="centered"
)

st.title("💼 Nova — AI Sales Assistant")
st.caption("Your smart international tech advisor, powered by LangGraph & OpenAI.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.markdown(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(msg.content)

# Handle user input
user_input = st.chat_input("Ask about our courses, tools, or pricing...")

if user_input:
    # Show user message
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append(HumanMessage(content=user_input))

    # Get assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = sales_agent_app.invoke({"messages": st.session_state.messages})
            latest_message = response["messages"][-1]
            st.markdown(latest_message.content)
            st.session_state.messages.append(latest_message)
