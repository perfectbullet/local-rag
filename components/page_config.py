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
        color: #000;
        font-size: 14px;
        font-weight: bold;
    }
    # .st-c2{
    #     background-color: rgb(255 255 255);
    # }
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
    .st-emotion-cache-ys1orn {
        width: 1544px;
        position: relative;
        display: flex;
        flex: 1 1 0%;
        flex-direction: column;
        gap: 0;
    }
    .st-emotion-cache-1gwvy71 h3 {
        font-size: 1.125rem;
        font-weight: 600;
        color: rgba(255, 255, 255, 0.95);
    }
    .st-emotion-cache-jkfxgf p {
        word-break: break-word;
        margin-bottom: 0px;
        font-size: 14px;
        color: rgba(255, 255, 255, 0.95);
    }
    .st-emotion-cache-1rsyhoq p {
        word-break: break-word;
        color: rgba(255, 255, 255, 0.95);
    }
    .st-emotion-cache-12h5x7g p {
        word-break: break-word;
        margin-bottom: 0px;
        color: rgba(255, 255, 255, 0.95);
    }
    </style>
    """,
        unsafe_allow_html=True,
    )
