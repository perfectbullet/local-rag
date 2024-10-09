import streamlit as st

from components.tabs.local_files import local_files
from components.tabs.github_repo import github_repo
from components.tabs.website import website


def sources():
    # st.title("直接导入您的数据")
    # st.markdown("**直接导入您的数据**")
    # st.caption("将您的数据转换为嵌入以便在聊天期间使用")
    st.write("")

    with st.expander("💻 &nbsp; **本地文件**", expanded=False):
        local_files()

    with st.expander("🗂️ &nbsp;**仓库数据**", expanded=False):
        github_repo()

    with st.expander("🌐 &nbsp; **网页数据**", expanded=False):
        website()
