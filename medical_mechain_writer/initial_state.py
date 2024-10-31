
def initial_state(st):

    if "full_response" not in st.session_state:
        st.session_state.full_response = ''
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "write_requirement" not in st.session_state:
        st.session_state.write_requirement = ''
    # if "query" not in st.session_state:
    #     st.session_state.query = ""
    # if "key_point" not in st.session_state:
    #     st.session_state.key_point = ""
    # if "key_words" not in st.session_state:
    #     st.session_state.key_words = ""
    # if "writing_requirements" not in st.session_state:
    #     st.session_state.writing_requirements = ""
    if "polish_target_content" not in st.session_state:
        st.session_state.polish_target_content = ""
    if "polish_requirements" not in st.session_state:
        st.session_state.polish_requirements = ""
    if "expand_target_content" not in st.session_state:
        st.session_state.expand_target_content = ""
    if "expand_requirements" not in st.session_state:
        st.session_state.expand_requirements = ""

    # button state
    if "start_write" not in st.session_state:
        st.session_state.start_write = False
    if "stop_generate" not in st.session_state:
        st.session_state.stop_generate = False
    if "start_export" not in st.session_state:
        st.session_state.start_export = False

    st.set_page_config(
        page_title="文案创作",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state='expanded',
    )
