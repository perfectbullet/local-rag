import streamlit as st


def set_page_header():
    st.header("医疗器械检索增强", anchor=False)
    st.caption(
        "使用大型语言模型(LLM)提取数据以进行检索增强生成(RAG)，所有这些都不需要第三方网络，避免敏感信息离开您的网络。"
    )
