import streamlit as st

import utils.helpers as func
import utils.rag_pipeline as rag
import utils.logs as logs


def github_repo():
    # st.header("Import files from a GitHub repo")
    # st.caption("Convert a GitHub repo to embeddings for utilization during chat")
    if st.session_state["selected_model"] is not None:
        st.text_input(
            "选择存储库",
            placeholder="jonfairbanks/local-rag",
            key="github_repo",
        )

        repo_processed = None
        repo_processed = st.button(
            "处理",
            on_click=func.clone_github_repo,
            args=(st.session_state["github_repo"],),
            key="process_github",
        )

        with st.spinner("处理中"):
            if repo_processed is True:
                # Initiate the RAG pipeline, providing documents to be saved on disk if necessary
                error = rag.rag_pipeline()
                
                if error is not None:
                    st.exception(error)
                else:
                    st.write("Your files are ready. Let's chat! 😎") # TODO: This should be a button.

    else:
        st.text_input(
            "选择存储库",
            placeholder="jonfairbanks/local-rag",
            disabled=True,
        )
        st.button(
            "处理仓库",
            disabled=True,
        )
