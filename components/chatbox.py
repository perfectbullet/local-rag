import streamlit as st

from utils.ollama import chat, context_chat


def chatbox():
    # 设定3列
    col1, col2 = st.columns([3, 1])
    # 设定不同的列标题和展示的内容
    with col1:
        # st.header("医疗器械检索增强")
        # st.caption(
        #     "使用大型语言模型(LLM)提取数据以进行检索增强生成(RAG)，所有这些都不需要第三方网络，避免敏感信息离开您的网络。"
        # )
        # st.header("请输入你要搜索的关键词")

        for msg in st.session_state["messages"]:
            print('msg is {}'.format(msg))
            st.chat_message(msg["role"]).write(msg["content"])
            # st.chat_message(msg["role"]).write_stream(generate_welcome_message(msg['content']))

        if prompt := st.chat_input("请输入你要搜索的关键词"):
            # Prevent submission if Ollama endpoint is not set
            if not st.session_state["query_engine"]:
                st.warning("Please confirm settings and upload files before proceeding.")
                st.stop()

            # Add the user input to messages state
            st.session_state["messages"].append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Generate llama-index stream with user input
            with st.chat_message("assistant"):
                with st.spinner("回答中..."):
                    response = st.write_stream(
                        # chat(
                        #     prompt=prompt
                        # )
                        context_chat(
                            prompt=prompt, query_engine=st.session_state["query_engine"]
                        )
                    )

            # Add the final response to messages state
            st.session_state["messages"].append({"role": "assistant", "content": response})
    with col2:
        st.header("帮助中心")
        # st.image("https://static.streamlit.io/examples/dog.jpg")
        # st.html()

        st.image("./static/images/help_04.png")
        st.image("./static/images/help_05.png")


