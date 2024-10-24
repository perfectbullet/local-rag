import streamlit as st
from streamlit_javascript import st_javascript

from components.sidebar import sidebar
from utils.logs import logger

def set_page_config():
    query_params = st.query_params
    logger.info('query_params is {}', query_params)
    if query_params.get('sidebar_state', '') == 'collapsed':
        # http://localhost:8503/?sidebar_state=collapsed&help=no-help
        sidebar_state = query_params.get('sidebar_state', '')
    else:
        sidebar_state = st.session_state["sidebar_state"]
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
     div[data-testid = "stSidebarHeader"]{
         background: url("/app/static/logo.png") no-repeat;
     }
     hr{
        margin:0;
    }
    button[data-testid="stBaseButton-secondary"]{
        padding: 0.25rem 1rem;
    }
    h2{
        padding: 0rem 0px;
        line-height: 1;
    }
    section[data-testid="stFileUploaderDropzone" ]{
        align-items: center !important;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # with open('ok.js', encoding='utf8') as f:
    #     script = f.read()
    #     print('script is ', script)
    # st_javascript(script)
