import os.path

import streamlit as st

from utils.langchain_rag_for_st import langchain_chat_stream
from utils.logs import logger


def chatbox():
    # 设定2列
    col1, col2 = st.columns([4, 1])
    # 设定不同的列标题和展示的内容
    with col1:
        with st.container(border=True):
            if prompt := st.chat_input("请输入你要搜索的关键词"):
                # Prevent submission if Ollama endpoint is not set
                logger.info('prompt is {}', prompt)
                # Generate llama-index stream with user input
                with st.container(border=True):
                    with st.chat_message("assistant"):
                        with st.spinner("回答中..."):
                            output_placeholder = st.empty()
                            # add refer source
                            source_placeholder = st.empty()
                            # Add assistant response to chat history
                            stream = langchain_chat_stream(prompt, st)
                            response = ""
                            for token in stream:
                                response += token
                                # print(chunk.choices[0].delta.content, end="")
                                output_placeholder.markdown(response)
                            source_txt = "### 参考文档如下："
                            seen_file_names = set()
                            for sc in st.session_state["sources"]:
                                logger.info('sc is {}', sc)
                                # ![local-rag-demo](http://localhost:8501/app/static/oktest_image_url//1446441727800.jpg)
                                base_url = 'http://localhost:8501/app/static/'
                                image_path = sc.get('image_path', '')
                                if image_path:
                                    image_markdown_url = '![{}]({}{})'.format(os.path.basename(image_path), base_url, image_path)
                                    source_txt += '\n\n**{}**\n\n{}'.format(sc['name'], image_markdown_url)
                                    source_placeholder.markdown(source_txt)
                                else:
                                    file_name = sc['name']
                                    if file_name in seen_file_names:
                                        continue
                                    seen_file_names.add(file_name)
                                    new_markdown_url = '({}pdf_and_doc/{})'.format(base_url, file_name)
                                    logger.info('file_markdown_url {}', new_markdown_url)
                                    source_txt += '\n\n[**{}**]{}\n\n'.format(file_name, new_markdown_url)
                                    logger.info('source_txt {}', source_txt)
                                    source_placeholder.markdown(source_txt)
                # Add the user input to messages state
                st.session_state["messages"].append({"role": "user", "content": prompt})
                # Add the final response to messages state
                st.session_state["messages"].append({"role": "assistant", "content": response})
                with st.container(border=True):
                    for msg in st.session_state["messages"]:
                        # log.info('msg is {}'.format(msg))
                        st.chat_message(msg["role"]).write(msg["content"])

        # st.caption('引用文档')
        # 这里我们设定一个高度为300的容器
        # with st.container(height=200):
        #     refer_div = '<div class="message">{}</div>'
        #     sources = st.session_state["sources"]
        #     source = '<br>'.join(sources)
        #     demo_txt = refer_div.format('{}'.format(source))
        #     st.html(demo_txt)

    with col2:
        # st.header("帮助中心")
        # st.image("https://static.streamlit.io/examples/dog.jpg")
        # st.html()
        # st.image("./static/images/help_04.png")
        with st.container(height=800):
            st.image("./static/help_center2.png")
