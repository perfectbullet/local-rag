import streamlit as st
from streamlit_modal import Modal

from components.tabs.local_files import local_files
from components.tabs.github_repo import github_repo
from components.tabs.website import website


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
            local_files()

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
