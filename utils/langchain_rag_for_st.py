import json
import os

import streamlit as st
from langchain_community.vectorstores import Chroma

from langchain_ollama import ChatOllama

from ddddddemo.rng_document import create_langchain_embedding_db, create_langchain_ollama_llm, rag_chat_stream
from utils.logs import logger


def get_langchain_embedding_db(
        ollama_base_url='http://127.0.0.1:11434',
        embedding_model="znbang/bge:large-zh-v1.5-f32",
        collection_name=None
) -> Chroma:

    vector_store = st.session_state.get('embedding_db')
    if not vector_store:
        logger.info('create vector_store collection_name is {}'.format(collection_name))
        vector_store = create_langchain_embedding_db(
            ollama_base_url=ollama_base_url,
            embedding_model=embedding_model,
            collection_name=collection_name
        )
        st.session_state['embedding_db'] = vector_store
    return vector_store


def get_langchain_ollama_llm() -> ChatOllama:
    llm = st.session_state.get('llm')
    if not llm:
        print('create llm')
        llm = create_langchain_ollama_llm()
        st.session_state['llm'] = llm
    return llm


def langchain_chat_stream(q, st):
    """
    Args:
        q: query
        st: st
    Returns:
        yield steam
    """
    sources = []
    collection_zh_name = st.session_state.get("selected_knowledge_base", "")
    embedding_model = st.session_state["embedding_model"]
    ollama_endpoint = st.session_state["ollama_endpoint"]
    collection_name = ''
    for kb in st.session_state["knowledge_base_config"]:
        if kb['knowledge_base_name'] == collection_zh_name:
            collection_name = kb['collection_dir']

    vector_store = create_langchain_embedding_db(
        ollama_base_url=ollama_endpoint,
        embedding_model=embedding_model,
        collection_name=collection_name
    )
    llm = get_langchain_ollama_llm()
    for chunk in rag_chat_stream(q, vector_store, llm):
        if a := chunk.get('answer'):
            yield a
        elif c := chunk.get('context'):
            for doc in c:
                if not doc.metadata.get('filetype'):
                    # 没有文件类型
                    source = doc.metadata['source']
                    sources.append(json.loads(source))
                else:
                    source_file = doc.metadata['source']
                    filetype = doc.metadata['filetype']
                    page = doc.metadata.get('page', 0)
                    new_source = {
                        'source': source_file,
                        'filetype': filetype,
                        'page': page,
                        'name': os.path.basename(source_file),
                    }
                    sources.append(new_source)

    st.session_state["sources"] = sources
