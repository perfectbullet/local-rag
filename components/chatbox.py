import streamlit as st

from utils.logs import logger
from utils.util_ollama import context_chat, chat

bot_template = """
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://cdn.icon-icons.com/icons2/1371/PNG/512/robot02_90810.png" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
"""


def chatbox():
    # 设定2列
    # st.image("./static/head_bg.png", width=2100)
    # st.html("")
    col1, col2 = st.columns([4, 1])
    # 设定不同的列标题和展示的内容
    with col1:
        with st.container(border=True, height=600):

            if prompt := st.chat_input("请输入你要搜索的关键词"):
                # Prevent submission if Ollama endpoint is not set
                logger.info('prompt is {}', prompt)
                logger.info('query_engine is {}', st.session_state["query_engine"])

                # if not st.session_state["query_engine"]:
                #     logger.warning('Please confirm settings and upload files before proceeding')
                #     st.warning("Please confirm settings and upload files before proceeding.")
                #     st.stop()
                # with st.chat_message("user"):
                #     st.markdown(prompt)

                # Generate llama-index stream with user input
                with st.container(border=True):
                    with st.chat_message("assistant"):
                        with st.spinner("回答中..."):
                            if st.session_state["query_engine"] is None:
                                response = st.write_stream(chat(prompt=prompt))
                            else:
                                response = st.write_stream(
                                    # chat(
                                    #     prompt=prompt
                                    # )
                                    context_chat(
                                        prompt=prompt, query_engine=st.session_state["query_engine"]
                                    )
                                )

                # st.chat_message(msg["role"]).write_stream(generate_welcome_message(msg['content']))
                logger.info('response is {}'.format(response))
                # Add the user input to messages state
                st.session_state["messages"].append({"role": "user", "content": prompt})
                # Add the final response to messages state
                st.session_state["messages"].append({"role": "assistant", "content": response})
                with st.container(border=True):
                    for msg in st.session_state["messages"]:
                        logger.info('msg is {}'.format(msg))
                        st.chat_message(msg["role"]).write(msg["content"])
        st.caption('引用文档')
        # 这里我们设定一个高度为300的容器
        with st.container(height=200):
            refer_div = '<div class="message">{}</div>'
            demo_txt = refer_div.format('来源:xxx.pdf<br>来源:xxx2.pdf')
            st.html(demo_txt)

    with col2:
        # st.header("帮助中心")
        # st.image("https://static.streamlit.io/examples/dog.jpg")
        # st.html()
        # st.image("./static/images/help_04.png")
        with st.container(height=800):
            st.image("./static/help_center2.png")
