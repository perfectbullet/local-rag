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

        knowledge_base_settings = st.container(border=True)
        with knowledge_base_settings:
            knowledge_base = st.selectbox(
                "专用领域模型",
                st.session_state["knowledge_base_list"],
                key="selected_knowledge_base",
            )
            logger.info('selected_knowledge_base is {}', st.session_state["selected_knowledge_base"])
            data_base_name = st.session_state['data_base_name']
            db_conn = sqlite3.connect(data_base_name)
            # INSERT OR REPLACE INTO users (id, name) VALUES (1, 'John');
            db_conn.execute(
                "INSERT OR REPLACE INTO session_state (state_name, state_value) VALUES (?, ?)",
                ('selected_knowledge_base', knowledge_base)
            )
            db_conn.commit()
            logger.info('knowledge_base is {}', knowledge_base)

        embedding_settings = st.container(border=True)
        with embedding_settings:
            embedding_model = st.selectbox(
                "嵌入模型",
                options=st.session_state['embedding_models'],
                # key="embedding_model",
            )
            if embedding_model == "Other":
                st.text_input(
                    "HuggingFace Model",
                    key="other_embedding_model",
                    placeholder="Salesforce/SFR-Embedding-Mistral",
                )
            if st.session_state["advanced"] == True:
                st.caption(
                    "View the [MTEB Embeddings Leaderboard](https://huggingface.co/spaces/mteb/leaderboard)"
                )
                st.text_input(
                    "Chunk Size",
                    help="Reducing `chunk_size` improves embedding precision by focusing on smaller text portions. This enhances information retrieval accuracy but escalates computational demands due to processing more chunks.",
                    key="chunk_size",
                    placeholder="1024",
                    value=st.session_state["chunk_size"],
                )
                st.text_input(
                    "Chunk Overlap",
                    help="The amount of overlap between two consecutive chunks. A higher overlap value helps maintain continuity and context across chunks.",
                    key="chunk_overlap",
                    placeholder="200",
                    value=st.session_state["chunk_overlap"],
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
