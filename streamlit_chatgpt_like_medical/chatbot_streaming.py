from openai import OpenAI
import streamlit as st

st.title("观想医疗v1")

client = OpenAI(
    api_key="sk-BhazmM2Qz12BXRYejKXMhibmTn2uuBrhOQv6bwcJgNVYBiBB",
    base_url="https://api.moonshot.cn/v1",
)

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("输入你的问题"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        stream = client.chat.completions.create(
            model="moonshot-v1-8k",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
