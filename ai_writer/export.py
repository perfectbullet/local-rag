import base64

import streamlit.components.v1 as components
from Markdown2docx import Markdown2docx
from loguru import logger


def download_button(object_to_download, download_filename):
    """
    Generates a link to download the given object_to_download.
    Params:
    ------
    object_to_download:  The object to be downloaded.
    download_filename (str): filename and extension of file. e.g. mydata.csv,
    Returns:
    -------
    (str): the anchor tag to download object_to_download
    """
    logger.info('start to download')
    b64 = base64.b64encode(object_to_download.read()).decode()
    mime_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

    with open('./static/jquery-3.2.1.min.js', 'rt') as f:
        js = f.read()
        dl_link = f"""
        <html>
        <head>
        <title>Start Auto Download file</title>
        <script>{js}</script>
        <script>
        $('<a href="data:{mime_type};base64,{b64}" download="{download_filename}">')[0].click()
        </script>
        </head>
        </html>
        """
        print(dl_link)
        return dl_link


def export(st):
    # 获取 Quill 编辑器中的文本
    latest_message = st.session_state.full_response
    logger.info('latest_message is {}'.format(latest_message))
    # 创建一个新的 Word 文档
    with open('tmp1215.md', 'wt', encoding='utf8') as f:
        f.write(latest_message)

    project = Markdown2docx('tmp1215')
    project.eat_soup()
    project.save()

    with open('tmp1215.docx') as f:
        components.html(
            download_button(f.buffer, 'outputv2.docx'),
            height=0,
        )
