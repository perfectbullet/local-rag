import streamlit as st
from components.sidebar import sidebar


def set_page_config():
    
    sidebar_state = st.session_state["sidebar_state"]
    print('sidebar_state is {}'.format(sidebar_state))

    st.set_page_config(
        # page_title="Local RAG",
        page_title="检索增强",
        page_icon="📚",
        layout="wide", 
        initial_sidebar_state=sidebar_state,
        # menu_items={},
    )

    ### Sidebar
    sidebar()

    # Remove the Streamlit `Deploy` button from the Header
    # 修改页面布局
    st.markdown(
        r"""
    <style>
    header[data-testid='stHeader'] {
       visibility: hidden;
    }
    header[data-testid='stHeader'] {
      display:none;
    }
    .st-emotion-cache-1jicfl2{
        padding:0px 5rem;
    }
    div[data-testid="stSidebarContent"]{
        background: #4582d3;
        color: white;
    }
    div[data-testid="stMarkdownContainer"]{
        color: #ffffff;
        font-size: 14px;
        font-weight: bold;
    }
    .st-c2{
        background-color: rgb(255 255 255);
    }
    button[data-testid="baseButton-headerNoPadding"] {
        path[fill='none']{
            fill: white;
        }
    }
    div[data-testid="stSidebarHeader"]{
        background: url("http://125.69.16.175:8502/media/b8cc86473a1f0794adfeee099753e8be097052c328f1e6741b2cab21.png");
    }
    </style>
    """,
        unsafe_allow_html=True,
    )
