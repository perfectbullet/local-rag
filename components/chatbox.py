import os.path

import streamlit as st

from ddddddemo.rng_document import query_keywords_in_file
from utils.langchain_rag_for_st import langchain_chat_stream
from utils.logs import logger
from config import STATIC_URL


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
                            html_source = '''<h3>参考文档如下：</h3>'''
                            seen_file_names = set()
                            for sc in st.session_state["sources"]:
                                logger.info('sc is {}', sc)
                                # ![local-rag-demo](http://localhost:8501/app/static/oktest_image_url//1446441727800.jpg)
                                # STATIC_URL
                                # STATIC_URL = 'http://127.0.0.1:8501/app/'
                                # base_url = 'http://localhost:8501/app/static/'
                                image_path = sc.get('image_path', '')
                                if image_path:
                                    image_markdown_url = '![{}]({}{})'\
                                        .format(os.path.basename(image_path), STATIC_URL, image_path)
                                    source_txt += '\n\n**{}**\n\n{}'.format(sc['name'], image_markdown_url)
                                    source_placeholder.markdown(source_txt)
                                else:
                                    file_name = sc['name']
                                    if file_name in seen_file_names:
                                        continue
                                    seen_file_names.add(file_name)
                                    new_markdown_url = '{}pdf_and_doc/{}'.format(STATIC_URL, file_name)
                                    logger.info('new_markdown_url is {}'.format(new_markdown_url))
                                    a_target = '''<a href="{}" download="{}">{}</a><br/>'''.format(new_markdown_url, file_name, file_name)
                                    # a_target = '''<a href="{}" rel="noopener noreferrer" download="{}">{}</a><br/>'''.format(new_markdown_url, file_name, file_name)
                                    html_source += a_target
                                    source_placeholder.html(html_source)

                                    # show item images
                                    item_images_placeholder = st.empty()
                                    file_path = os.path.join('./static/pdf_and_doc/', file_name)
                                    # [('static/item_images/0945375522.jpg', '0945375522.jpg', '雾化设备'), ('static/item_images/0957281322.jpg', '0957281322.jpg', '辅助生殖器械')]
                                    seen_key_words = query_keywords_in_file(
                                        file_path,
                                        user_input=prompt,
                                        st=st
                                    )
                                    item_image_urls_markdown = ''
                                    for keyword in seen_key_words:
                                        item_image_url = '![{}]({}{})'.format(keyword[2], STATIC_URL, keyword[0])
                                        logger.info(item_image_url)
                                        item_image_urls_markdown += '\n\n**{}**\n\n{}'.format(keyword[2], item_image_url)
                                    item_images_placeholder.markdown(item_image_urls_markdown)

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
