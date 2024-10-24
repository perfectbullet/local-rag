import sqlite3
import streamlit as st

from utils.logs import logger
from utils.helpers import get_knowledge_base

from utils.util_ollama import get_models, get_embedding_models
from config import OLLAMA_BASE_URL


def set_initial_state():
    if 'data_base' not in st.session_state:
        data_base_name = 'local_rag.db'
        conn = sqlite3.connect(data_base_name)
        # 创建一个表
        cur = conn.cursor()
        cur.execute('''
        CREATE TABLE IF NOT EXISTS file_list (
            id INTEGER PRIMARY KEY,
            filename TEXT NOT NULL,
            filetype TEXT NOT NULL,
            knowledge_base TEXT NOT NULL,
            embedded BOOLEAN NOT NULL
        )
        ''')
        cur.execute('''
                CREATE TABLE IF NOT EXISTS session_state (
                    id INTEGER PRIMARY KEY,
                    state_name TEXT UNIQUE NOT NULL,
                    state_value TEXT NOT NULL
                )
                ''')
        cur.execute('''
                        CREATE TABLE IF NOT EXISTS keywords_to_image (
                            id INTEGER PRIMARY KEY,
                            image_path TEXT UNIQUE NOT NULL,
                            image_name TEXT NOT NULL,
                            keywords TEXT NOT NULL
                        )
                        ''')
        conn.commit()
        st.session_state["data_base_name"] = data_base_name

    ###########
    # General #
    ###########
    if "knowledge_base_list" not in st.session_state:
        logger.info('init knowledge base')
        get_knowledge_base()
    if 'selected_knowledge_base' not in st.session_state:
        logger.info('selected_knowledge_base not in st.session_state')
        data_base_name = st.session_state['data_base_name']
        # 数据库对象不能跨线程使用
        db_conn = sqlite3.connect(data_base_name)
        cur = db_conn.cursor()
        # 文件名称和知识库联合不能重复
        sql_text_q = "SELECT state_name,state_value FROM session_state WHERE state_name=?"
        logger.info('sql_text_q is {}'.format(sql_text_q))
        cur.execute(sql_text_q, ('selected_knowledge_base', ))
        # 获取查询结果
        st_state = cur.fetchone()
        logger.info('fetrest is {}'.format(st_state))
        if st_state:
            st.session_state["selected_knowledge_base"] = st_state[1]
        else:
            st.session_state["selected_knowledge_base"] = st.session_state["knowledge_base_list"][0]

    if "collection_name" not in st.session_state:
        st.session_state["collection_name"] = None

    if "sources" not in st.session_state:
        st.session_state["sources"] = []

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

    ################################
    #  Files, Documents & Websites #
    ################################

    if "file_list" not in st.session_state:
        st.session_state["file_list"] = []

    if "github_repo" not in st.session_state:
        st.session_state["github_repo"] = None

    if "websites" not in st.session_state:
        st.session_state["websites"] = []

    ###############
    # Llama-Index #
    ###############

    if "llm" not in st.session_state:
        st.session_state["llm"] = None

    if "documents" not in st.session_state:
        st.session_state["documents"] = None

    if "query_engine" not in st.session_state:
        st.session_state["query_engine"] = None

    if "chat_mode" not in st.session_state:
        st.session_state["chat_mode"] = "compact"

    #####################
    # Advanced Settings #
    #####################

    if "advanced" not in st.session_state:
        st.session_state["advanced"] = False

    if "system_prompt" not in st.session_state:
        sys_prompt = """您是一个复杂的虚拟助手，旨在帮助用户全面理解和提取他们可以使用的各种文档的见解。您的专长在于处理复杂的查询并根据这些文件中包含的信息提供有洞察力的分析。"""
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
