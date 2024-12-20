import sqlite3
import streamlit as st

from utils.logs import logger

from utils.util_ollama import get_models, get_embedding_models
from config import OLLAMA_BASE_URL
from medical_components.sources import sources
from medical_components.settings import settings


def sidebar():
    with st.sidebar:
        with st.container(border=True):
            sources()
        settings()


def set_initial_state():
    if 'data_base' not in st.session_state:
        data_base_name = 'medical_llm_rag.db'
        conn = sqlite3.connect(data_base_name)
        # 创建一个表
        cur = conn.cursor()
        cur.execute('''
                CREATE TABLE IF NOT EXISTS session_state (
                    id INTEGER PRIMARY KEY,
                    state_name TEXT UNIQUE NOT NULL,
                    state_value TEXT NOT NULL
                )
                ''')
        conn.commit()
        st.session_state["data_base_name"] = data_base_name

    ###########
    # General #
    ###########
    if "last_chat_input" not in st.session_state:
        st.session_state["last_chat_input"] = '请输入你要搜索的关键词'

    if "sidebar_state" not in st.session_state:
        st.session_state["sidebar_state"] = "expanded"

    if "ollama_endpoint" not in st.session_state:
        st.session_state["ollama_endpoint"] = OLLAMA_BASE_URL

    if "embedding_models" not in st.session_state:
        embedding_models = get_embedding_models()
        logger.info('embedding_models is {}'.format(embedding_models))
        st.session_state["embedding_models"] = get_embedding_models()

    if "ollama_models" not in st.session_state:
        try:
            models = get_models()
            st.session_state["ollama_models"] = models
        except Exception:
            st.session_state["ollama_models"] = []
            pass

    if "selected_model" not in st.session_state:
        try:
            if "qwen2.5:14b" in st.session_state["ollama_models"]:
                st.session_state["selected_model"] = (
                    "qwen2.5:14b"  # Default to qwen2.5:14b on initial load
                )
            elif "qwen2.5:latest" in st.session_state["ollama_models"]:
                st.session_state["selected_model"] = (
                    "qwen2.5:latest"
                )
            elif "llama3:8b" in st.session_state["ollama_models"]:
                st.session_state["selected_model"] = (
                    "llama3:8b"  # Default to llama3:8b on initial load
                )
            elif "llama2:7b" in st.session_state["ollama_models"]:
                st.session_state["selected_model"] = (
                    "llama2:7b"  # Default to llama2:7b on initial load
                )
            else:
                st.session_state["selected_model"] = st.session_state["ollama_models"][
                    0
                ]  # If llama2:7b is not present, select the first model available
        except Exception:
            st.session_state["selected_model"] = None
            pass

    if "messages" not in st.session_state:
        st.session_state["messages"] = [

        ]


    #####################
    # Advanced Settings #
    #####################
    if "advanced" not in st.session_state:
        st.session_state["advanced"] = False

    if "system_prompt" not in st.session_state:
        sys_prompt = """"""
        st.session_state['system_prompt'] = sys_prompt
        # st.session_state["system_prompt"] = (
        #     "You are a sophisticated virtual assistant designed to assist users in comprehensively understanding and extracting insights from a wide range of documents at their disposal. Your expertise lies in tackling complex inquiries and providing insightful analyses based on the information contained within these documents."
        # )

    if "top_k" not in st.session_state:
        st.session_state["top_k"] = 3

    if "embedding_model" not in st.session_state:
        st.session_state["embedding_model"] = st.session_state["embedding_models"][0]

    if "other_embedding_model" not in st.session_state:
        st.session_state["other_embedding_model"] = None

    if "chunk_size" not in st.session_state:
        st.session_state["chunk_size"] = 1024

    if "chunk_overlap" not in st.session_state:
        st.session_state["chunk_overlap"] = 200
