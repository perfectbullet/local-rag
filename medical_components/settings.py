import json
import sqlite3

import streamlit as st
import utils.util_ollama as ollama
from datetime import datetime

from utils.logs import logger


def settings():
    st.subheader('基础配置')
    with st.container(border=True):
        chat_settings = st.container(border=True)
        with chat_settings:
            st.text_input(
                "服务器地址",
                key="ollama_endpoint",
                placeholder="http://localhost:11434",
                on_change=ollama.get_models,
            )
        with st.container(border=True):
            st.selectbox(
                "基础模型",
                st.session_state["ollama_models"],
                key="selected_model",
                disabled=len(st.session_state["ollama_models"]) == 0,
                placeholder="Select Model" if len(st.session_state["ollama_models"]) > 0 else "No Models Available",
            )
        export_data_settings = st.container(border=True)
        with export_data_settings:
            st.write("导出历史数据")
            st.download_button(
                label="下载",
                data=json.dumps(st.session_state["messages"]),
                file_name=f"local-rag-chat-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.json",
                mime="application/json",
            )

    st.toggle("高级设置", key="advanced")

    if st.session_state["advanced"] == True:
        with st.expander("Current Application State"):
            state = dict(sorted(st.session_state.items()))
            st.write(state)
