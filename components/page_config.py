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
        padding:0px 0rem;
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
        background: url("/app/static/logo.png");
    }
    .st-emotion-cache-1nuoks4 {
        width: 1512px;
        position: relative;
        display: flex;
        flex: 1 1 0%;
        flex-direction: column;
        gap: 0rem;
    }
    .st-emotion-cache-1srxgaf {
        width: 1544px;
        position: relative;
        gap: 0rem;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )
