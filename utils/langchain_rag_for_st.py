import streamlit as st
from langchain_community.vectorstores import Chroma

from langchain_ollama import ChatOllama

from ddddddemo.rng_document import create_langchain_embedding_db, create_langchain_ollama_llm, rag_chat_stream
from utils.logs import logger


def get_langchain_embedding_db(collection_name=None) -> Chroma:

    vector_store = st.session_state.get('embedding_db')
    if not vector_store:
        logger.info('create vector_store collection_name is {}'.format(collection_name))
        vector_store = create_langchain_embedding_db(collection_name=collection_name)
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

    vector_store = get_langchain_embedding_db(collection_name='oktest_image_url_local_image')
    llm = get_langchain_ollama_llm()
    for chunk in rag_chat_stream(q, vector_store, llm):
        if a := chunk.get('answer'):
            yield a
        elif c := chunk.get('context'):
            for doc in c:
                source = doc.metadata['source']
                sources.append(source)
    st.session_state["sources"] = sources
