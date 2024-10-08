import streamlit as st

from datetime import datetime


def about():
    st.title("📚 本地 RAG")
    st.caption(f"GX软件部ZJ开发 &copy; {datetime.now().year}")
    st.write("")

    links_html = """
    <ul style="list-style-type:none; padding-left:0;">
        <li>
            <a href="https://github.com/jonfairbanks/local-rag" style="color: grey;">GitHub</a>
        </li>
        <li>
            <a href="https://hub.docker.com/r/jonfairbanks/local-rag" style="color: grey;">Docker Hub</a>
        </li>
    </ul>
    """

    resources_html = """
    <ul style="list-style-type:none; padding-left:0;">
        <li>
            <a href="https://blogs.nvidia.com/blog/what-is-retrieval-augmented-generation/" style="color: grey;">
                什么是 RAG？
            </a>
        </li>
        <li>
            <a href="https://aws.amazon.com/what-is/embeddings-in-machine-learning/" style="color: grey;">
                什么是嵌入？
            </a>
        </li>
    </ul>
    """

    help_html = """
    <ul style="list-style-type:none; padding-left:0;">
        <li>
            <a href="https://github.com/jonfairbanks/local-rag/issues" style="color: grey;">
                Bug报告
            </a>
        </li>
        <li>
            <a href="https://github.com/jonfairbanks/local-rag/discussions/new?category=ideas" style="color: grey;">
                建议
            </a>
        </li>
    </ul>
    """

    st.subheader("链接")
    st.markdown(links_html, unsafe_allow_html=True)

    st.subheader("资源")
    st.markdown(resources_html, unsafe_allow_html=True)

    st.subheader("帮助")
    st.markdown(help_html, unsafe_allow_html=True)
