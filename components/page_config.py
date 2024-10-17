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
    div[data-testid="stSidebarHeader"]{
        background: url("/app/static/logo.png");
    }
    </style>
    """,
        unsafe_allow_html=True,
    )
