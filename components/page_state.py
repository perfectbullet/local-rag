import streamlit as st

import utils.logs as logs

from utils.ollama import get_models

gx_ollama = 'http://125.69.16.175:11434'
zj_ollama = "http://localhost:11434"


def set_initial_state():

    ###########
    # General #
    ###########

    if "sidebar_state" not in st.session_state:
        st.session_state["sidebar_state"] = "expanded"

    if "ollama_endpoint" not in st.session_state:
        st.session_state["ollama_endpoint"] = gx_ollama

    if "embedding_model" not in st.session_state:
        st.session_state["embedding_model"] = "Default (bge-large-en-v1.5)"

    if "ollama_models" not in st.session_state:
        try:
            models = get_models()
            st.session_state["ollama_models"] = models
        except Exception:
            st.session_state["ollama_models"] = []
            pass

    if "selected_model" not in st.session_state:
        try:
            if "llama3:8b" in st.session_state["ollama_models"]:
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
        st.session_state["embedding_model"] = None

    if "other_embedding_model" not in st.session_state:
        st.session_state["other_embedding_model"] = None

    if "chunk_size" not in st.session_state:
        st.session_state["chunk_size"] = 1024

    if "chunk_overlap" not in st.session_state:
        st.session_state["chunk_overlap"] = 200
