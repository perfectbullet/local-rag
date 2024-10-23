import os.path

import streamlit as st

from utils.langchain_rag_for_st import langchain_chat_stream
from utils.logs import logger


def chatbox():
    # 设定2列
    query_params = st.query_params
    logger.info('query_params is {}', query_params)
    show_help = query_params.get('help', '')
    if show_help != 'no-help':
        col1, col2 = st.columns([4, 1])
    else:
        col1, col2 = st.columns([1000, 1])
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
                                    # logger.info('file_markdown_url {}', new_markdown_url)
                                    # source_txt += '\n\n[**{}**]{}\n\n'.format(file_name, new_markdown_url)
                                    # logger.info('source_txt {}', source_txt)
                                    # source_placeholder.markdown(source_txt)
                                    a_target = '''<a href="{}" download="{}">{}</a>'''.format(new_markdown_url,
                                                                                              file_name, file_name)
                                    source_placeholder.html(a_target)

                # Add the user input to messages state
                st.session_state["messages"].append({"role": "user", "content": prompt})
                # Add the final response to messages state
                st.session_state["messages"].append({"role": "assistant", "content": response})
                with st.container(border=True):
                    for msg in st.session_state["messages"]:
                        # log.info('msg is {}'.format(msg))
                        st.chat_message(msg["role"]).write(msg["content"])
    with col2:
        query_params = st.query_params
        logger.info('query_params is {}', query_params)
        show_help = query_params.get('help', '')
        if show_help != 'no-help':
            with st.container(height=800):
                st.image("./static/help_center2.png")
