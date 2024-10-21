import os

import sqlite3
import time

import streamlit as st

from ddddddemo.rng_document import create_langchain_embedding_db, load_pdf, load_pdf_page, add_document
from utils.helpers import save_uploaded_file
from utils.logs import logger


supported_files_new = (
    "csv",
    "docx",
    "md",
    "pdf",
    "txt",
)


def rag_pipeline(uploaded_files: list = None):
    """
    """
    data_base_name = st.session_state['data_base_name']
    # 数据库对象不能跨线程使用
    db_conn = sqlite3.connect(data_base_name)
    # 当前使用的领域知识库
    collection_zh_name = st.session_state.get("selected_knowledge_base", "")
    new_saved_files = []
    # 1. 保存文件到磁盘
    if uploaded_files is not None:
        save_dir =  "./data"
        os.makedirs(save_dir, exist_ok=True)
        logger.info('save dir is {}'.format(save_dir))

        for uploaded_file in uploaded_files:
            file_name = uploaded_file.name
            # 查询已有的
            cur = db_conn.cursor()
            # 文件名称和知识库联合不能重复
            sql_text_q = "SELECT filename FROM file_list WHERE filename=? and knowledge_base=?"
            logger.info('sql_text_q is {}'.format(sql_text_q))
            cur.execute(sql_text_q, (file_name, collection_zh_name))
            # 获取查询结果
            fetrest = cur.fetchone()
            logger.info('fetrest is {}'.format(fetrest))

            if fetrest:
                st.info(f"{file_name} 已上传过")
                continue
            else:
                with st.spinner(f"处理中 {file_name}..."):
                    save_uploaded_file(uploaded_file, save_dir)
                    new_saved_files.append(file_name)
                    st.info(f"{file_name} 保存成功")

    # 2. 从data目录加载文档
    logger.info(f"选择了领域数据库: {collection_zh_name}")
    logger.info('collection_zh_name is {}', collection_zh_name)
    collection_name = ''
    for kb in st.session_state["knowledge_base_config"]:
        if kb['knowledge_base_name'] == collection_zh_name:
            collection_name = kb['collection_dir']
    if not collection_name:
        st.warning('没有选择专业领域模型')
        st.stop()

    ollama_endpoint = st.session_state["ollama_endpoint"]
    embedding_model = st.session_state["embedding_model"]
    logger.info('ollama_endpoint is {}', ollama_endpoint)
    logger.info('embedding_model is {}', embedding_model)

    vector_store = create_langchain_embedding_db(
        ollama_base_url=ollama_endpoint,
        embedding_model=embedding_model,
        collection_name=collection_name
    )
    for fname in new_saved_files:
        file_path = os.path.join(save_dir, fname)
        logger.info('file name is {}', fname)
        if fname.endswith('pdf'):
            logger.info('file_path {}', file_path)
            # pdf_docs = load_pdf(file_path)
            # 按页加载pdf
            pdf_docs = load_pdf_page(file_path)
            ok_pdf_docs = []
            for doc in pdf_docs:
                doc.metadata['filetype'] = 'pdf'
                if len(doc.page_content) < 10:
                    # 过滤掉空的页
                    continue
                ok_pdf_docs.append(doc)
            logger.info('pdf_docs  is {}', pdf_docs)
            ids = add_document(vector_store, pdf_docs)
            db_conn.execute(
                "INSERT INTO file_list (filename, filetype, knowledge_base, embedded) VALUES (?, ?, ?, ?)",
                (fname, 'pdf', collection_zh_name, True)
            )
            db_conn.commit()
            st.info("{}上传到: {}".format(fname, collection_zh_name))
    db_conn.close()
    st.info("✔️ 上传完成")


def langchain_local_files():
    """
    基于 langchain的 local files
    Returns:
    """
    uploaded_files = st.file_uploader(
        "选择文件",
        accept_multiple_files=True,
        type=supported_files_new,
    )

    if len(uploaded_files) > 0:
        st.session_state["file_list"] = uploaded_files

        with st.spinner("处理中..."):
            # Initiate the RAG pipeline, providing documents to be saved on disk if necessary
            time.sleep(3)
            rag_pipeline(uploaded_files)
            # Display errors (if any) or proceed
            st.info("上传完成")
