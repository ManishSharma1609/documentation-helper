import os
from dotenv import load_dotenv
from backend.core import query_LLM
from typing import Set
import streamlit as st
from streamlit_chat import message

load_dotenv()
os.environ["LANGCHAIN_TRACING_V2"]=os.getenv("LANGCHAIN_TRACING_V2")
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")


st.header("Documentation Helper Bot")

prompt = st.text_input("Prompt", placeholder="Enter Your Prompt here...")

if (
    "user_prompt_history" not in st.session_state
    and "chat_answer_history" not in st.session_state
    and "chat_history" not in st.session_state
):
    st.session_state["user_prompt_history"] = []
    st.session_state["chat_answer_history"] = []
    st.session_state["chat_history"] = []

def create_source_string(source_url: Set[str]) -> str:
    if not source_url:
        return ""

    sources_list = list(source_url)
    sources_list.sort()
    source_string = "Sources:\n"

    for i, source in enumerate(sources_list):
        source_string += f"{i+ 1}. {source}\n"

    return source_string


if prompt:
    with st.spinner("Generating response..."):
        generated_response = query_LLM(query=prompt, chat_history = st.session_state["chat_history"])
        sources = set(
            [doc.metadata["source"] for doc in generated_response["source_documents"]]
        )
        formatted_response = (
            f"{generated_response["result"]} \n\n {create_source_string(sources)}"
        )

        st.session_state["user_prompt_history"].append(prompt)
        st.session_state["chat_answer_history"].append(formatted_response)
        st.session_state["chat_history"].append(("human", prompt))
        st.session_state["chat_history"].append(("ai", generated_response["result"]))

if st.session_state["user_prompt_history"]:
    for generated_response, user_query in zip(
        st.session_state["chat_answer_history"], st.session_state["user_prompt_history"]
    ):
        message(user_query, is_user=True)
        message(generated_response)
