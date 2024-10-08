import os
import shutil

import streamlit as st

import utils.helpers as func
import utils.ollama as ollama
import utils.llama_index as llama_index
import utils.logs as logs
import utils.rag_pipeline as rag

# supported_files = (
#     "csv",
#     "docx",
#     "epub",
#     "ipynb",
#     "json",
#     "md",
#     "pdf",
#     "ppt",
#     "pptx",
#     "txt",
# )

supported_files_new = (
    "csv",
    "docx",
    "md",
    "pdf",
    "txt",
)


def local_files():
    # Force users to confirm Settings before uploading files
    if st.session_state["selected_model"] is not None:
        uploaded_files = st.file_uploader(
            "选择文件22",
            accept_multiple_files=True,
            type=supported_files_new,
        )
    else:
        # st.warning("Please configure Ollama settings before proceeding!", icon="⚠️")
        st.warning("请先配置 Ollama 设置然后再继续！", icon="⚠️")
        file_upload_container = st.container(border=True)
        with file_upload_container:
            uploaded_files = st.file_uploader(
                "选择文件33",
                accept_multiple_files=True,
                type=supported_files,
                disabled=True,
            )

    if len(uploaded_files) > 0:
        st.session_state["file_list"] = uploaded_files

        with st.spinner("处理中..."):
            # Initiate the RAG pipeline, providing documents to be saved on disk if necessary
            error = rag.rag_pipeline(uploaded_files)

            # Display errors (if any) or proceed
            if error is not None:
                st.exception(error)
            else:
                st.write("您的文件已准备好") # TODO: This should be a button.
