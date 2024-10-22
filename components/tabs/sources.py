import sqlite3

import pandas as pd
import streamlit as st
from streamlit import header
from streamlit_modal import Modal

from components.tabs.local_files_langchain import langchain_local_files
from components.tabs.github_repo import github_repo
from components.tabs.website import website
from utils.logs import logger


def sources():
    # 定义 local file modal
    modal = Modal(
        "💻 &nbsp;",
        key="demo-modal",
        # Optional
        padding=20,  # default value
        max_width=744  # default value
    )
    open_modal = st.button("💻 &nbsp; **本地文件集**")
    if open_modal:
        modal.open()
    if modal.is_open():
        with modal.container():
            # with st.expander("💻 &nbsp; **本地文件**", expanded=True):
            langchain_local_files()

    # 展示已导入数据
    show_data_modal = Modal(
        "💻已导入数据 &nbsp;",
        key="show_data_modal",
        # Optional
        padding=20,  # default value
        max_width=744  # default value
    )
    show_data_button = st.button("💻 &nbsp; **查看数据**")
    if show_data_button:
        show_data_modal.open()
    if show_data_modal.is_open():
        with show_data_modal.container():
            data_base_name = st.session_state['data_base_name']
            db_conn = sqlite3.connect(data_base_name)
            collection_zh_name = st.session_state["selected_knowledge_base"]
            logger.info('collection_zh_name is {}', collection_zh_name)
            cur = db_conn.cursor()
            sql_text_q = "SELECT filename,filetype,knowledge_base FROM file_list WHERE knowledge_base=?"
            logger.info('sql_text_q is {}'.format(sql_text_q))
            cur.execute(sql_text_q, (collection_zh_name,))
            fetch_all_files = cur.fetchall()
            if fetch_all_files:
                logger.info('fetch_all_files is {}'.format(fetch_all_files))
                df = pd.DataFrame(fetch_all_files)
                # 添加表头
                df.columns = ['文件名', '文件类型', '专业领域模型名称']
                st.table(df)
            else:
                st.subheader('还未导入数据')

    # databae modal
    data_base_modal = Modal(
        "💻 &nbsp;",
        key="data_base_modal",
        # Optional
        padding=20,  # default value
        max_width=744  # default value
    )
    data_base_modal_button = st.button("🗂️ &nbsp;**仓库数据**")
    if data_base_modal_button:
        data_base_modal.open()
    if data_base_modal.is_open():
        with data_base_modal.container():
            # with st.expander("🗂️ &nbsp;**仓库数据**", expanded=True):
            github_repo()

    # web modal
    web_modal = Modal(
        "🌐 &nbsp;",
        key="web_modal",
        # Optional
        padding=20,  # default value
        max_width=744  # default value
    )
    data_base_modal_button = st.button("🌐 &nbsp; **网页数据**")
    if data_base_modal_button:
        web_modal.open()
    if web_modal.is_open():
        with web_modal.container():
            website()
