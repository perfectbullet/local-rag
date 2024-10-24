import streamlit as st
import os
from openai import OpenAI
import streamlit.components.v1 as components
import time
import re
from functools import partial
from streamlit_quill import st_quill

# App title
st.set_page_config(page_title="✏️AI Writer", layout="wide")

import re
from collections import defaultdict


def parse_markdown(md_filepath):
    markdown_text = ''
    with open(md_filepath, 'r') as f:
        for l in f.readlines():
            markdown_text += l
    # 结构化数据存储
    structured_data = defaultdict(lambda: defaultdict(str))

    # 正则表达式匹配标题
    h1_pattern = re.compile(r'^## (.+)', re.MULTILINE)
    h2_pattern = re.compile(r'^### (.+)', re.MULTILINE)

    # 查找所有一级标题
    h1_matches = list(h1_pattern.finditer(markdown_text))

    for i, h1_match in enumerate(h1_matches):
        h1_title = h1_match.group(1).strip()
        h1_start = h1_match.end()
        h1_end = h1_matches[i + 1].start() if i + 1 < len(h1_matches) else len(markdown_text)

        # 获取一级标题下的内容
        h1_content = markdown_text[h1_start:h1_end]

        # 查找所有二级标题
        h2_matches = list(h2_pattern.finditer(h1_content))

        if not h2_matches:
            # 如果没有二级标题，直接存储一级标题的内容
            structured_data[h1_title] = h1_content.strip()
        else:
            for j, h2_match in enumerate(h2_matches):
                h2_title = h2_match.group(1).strip()
                h2_start = h2_match.end()
                h2_end = h2_matches[j + 1].start() if j + 1 < len(h2_matches) else len(h1_content)

                # 获取二级标题下的内容
                h2_content = h1_content[h2_start:h2_end].strip()

                # 去除二级标题本身的行
                h2_content = re.sub(r'^## .+', '', h2_content, flags=re.MULTILINE).strip()

                # 存储二级标题及其内容
                structured_data[h1_title][h2_title] = h2_content

    return structured_data


# client = OpenAI(
#         api_key="sk-60f7dab83508414f94ec5c9c86751c53", # 如果您没有配置环境变量，请在此处用您的API Key进行替换
#         base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")
client = OpenAI(
    api_key='None', base_url="http://localhost:18400/v1"
)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "query" not in st.session_state:
    st.session_state.query = ""
if "key_point" not in st.session_state:
    st.session_state.key_point = ""
if "key_words" not in st.session_state:
    st.session_state.key_words = ""
if "writing_requirements" not in st.session_state:
    st.session_state.writing_requirements = ""
if "polish_target_content" not in st.session_state:
    st.session_state.polish_target_content = ""
if "polish_requirements" not in st.session_state:
    st.session_state.polish_requirements = ""
if "expand_target_content" not in st.session_state:
    st.session_state.expand_target_content = ""
if "expand_requirements" not in st.session_state:
    st.session_state.expand_requirements = ""


# Function for generating LLaMA2 response
def init_write(query, key_words, key_point, writing_requirements, structured_data):
    toc = []
    for h1, h2_data in structured_data.items():
        toc.append(h1)
        if not isinstance(h2_data, str):
            for h2, content in h2_data.items():
                toc.append(h2)
    toc = '\n'.join(toc)

    system = f"""
    ## 角色描述：你是一名项目写作专家，能根据项目主题和给定的文档模板的目录结构，生成完整的项目《立项申请书》。
## 工作流程
第一步：在开始撰写文章之前，必须认真阅读并牢记给定文档模板的目录结构。
第二步：使用Markdown格式，作为专家文章作者，撰写一篇完全详细、长篇、100%独特、创意且人性化的信息性文章，至少2000字。文章应以正式、信息丰富和乐观的语气撰写。
必须阅读以下所有信息。

请使用{query}作为项目主题，并在每个标题下撰写至少400-500字的引人入胜的段落。
## 要求
- 符合{query}的主题，可以适度扩散
- 本项目的关键词有如下几个:{key_words}
- 必须包含以下的要点: {key_point}
- 请遵循以下的写作要求:{writing_requirements}

## 模板目录结构
```text
{toc}
```
"""
    #     user = f"""
    # ## 模板目录结构
    # ```markdown
    # # 一、项目简介
    # # 二、必要性
    # ## （一）立项背景
    # ## （二）申报依据
    # # 三、主要研究内容及应用前景分析
    # ## （一）研究目标
    # ## （二）研究内容
    # ## （三）成果形式
    # ## （四）技术指标
    # # 四、初步方案
    # ## （一）总体方案
    # ## （二）研制周期
    # ## （三）项目组组成
    # # 五、经费概算和年度安排
    # ## （一）科研项目经费预算表
    # ## （二）项目直接经费预算明细表
    # ```
    # 项目名称:{query}
    #     """
    all_outputs = []
    for h1, h2_data in structured_data.items():
        all_outputs.append(f'\n## {h1}\n')
        if isinstance(h2_data, str):
            user = f"""
                请开始写二级章节`{h1}`。我为你准备了一些可供参考的内容来辅助你写作。你可以参考其中的篇章分布和语言风格。
    供参考的内容如下:
    ```text
    {h2_data}
    ```
    ## 注意：如果供参考的内容与项目主题和项目关键词等不相关，请不必参考，自行编写。
    """
            messages = []
            messages.append({'role': 'system', 'content': system})
            messages.append({'role': 'user', 'content': user})
            # for dict_message in st.session_state.messages:
            #     if dict_message["role"] == "user":
            #         messages.append({'role': 'user','content': dict_message["content"]})
            #     else:
            #         messages.append({'role': 'assistant','content': dict_message["content"]})

            output = client.chat.completions.create(
                # model="qwen-plus",
                model="qwen7b",
                messages=messages,
                stream=True,
                # 可选，配置以后会在流式输出的最后一行展示token使用信息
                stream_options={"include_usage": False}
            )
            all_outputs.append(output)
        else:
            for h2, content in h2_data.items():
                user = f"""
                请开始写二级章节`{h1}`的三级小章节`{h2}`。我为你准备了一些可供参考的内容来辅助你写作。你可以参考其中的篇章分布和语言风格。
    供参考的内容如下:
    ```text
    {content}
    ```
    ## 注意：如果供参考的内容与项目主题和项目关键词等不相关，请不必参考，自行编写。

    请以`## {h2}`为开头，输出写作的内容。
    """
                messages = []
                messages.append({'role': 'system', 'content': system})
                messages.append({'role': 'user', 'content': user})
                # for dict_message in st.session_state.messages:
                #     if dict_message["role"] == "user":
                #         messages.append({'role': 'user','content': dict_message["content"]})
                #     else:
                #         messages.append({'role': 'assistant','content': dict_message["content"]})

                output = client.chat.completions.create(
                    # model="qwen-plus",
                    model='qwen7b',
                    messages=messages,
                    stream=True,
                    # 可选，配置以后会在流式输出的最后一行展示token使用信息
                    stream_options={"include_usage": False}
                )
                all_outputs.append(output)
    return all_outputs


def rewrite_polish(selected_text, polish_requirements):
    system = """ ## 角色描述：你是一名项目写作专家，擅长对项目申请书中的文字进行润色。
## 工作流程
第一步：在开始润色之前，必须认真阅读并牢记润色的要求。
第二步：使用Markdown格式，按照润色的要求，对给你的文字进行润色。
    """
    user = f"""
原文字如下:
{selected_text}
润色要求如下:
{polish_requirements}
    """
    messages = []
    messages.append({'role': 'system', 'content': system})
    messages.append({'role': 'user', 'content': user})

    output = client.chat.completions.create(
        # model="qwen-plus",
        model="qwen7b",
        messages=messages,
        stream=True,
        n=3
    )
    return output


def rewrite_expand(selected_text, polish_requirements):
    system = """ ## 角色描述：你是一名项目写作专家，擅长对项目申请书中的文字进行扩写。
## 工作流程
第一步：在开始扩写之前，必须认真阅读并牢记扩写的要点。
第二步：使用Markdown格式，按照扩写的要求，对给你的文字进行扩写。
    """
    user = f"""
原文字如下:
{selected_text}
扩写的要点如下:
{polish_requirements}
    """
    messages = []
    messages.append({'role': 'system', 'content': system})
    messages.append({'role': 'user', 'content': user})

    output = client.chat.completions.create(
        # model="qwen-plus",
        model="qwen7b",
        messages=messages,
        # max_tokens=500,
        stream=True,
        n=3,
        # temperature=1.5,
        # top_p=0.9,
        # 可选，配置以后会在流式输出的最后一行展示token使用信息
        stream_options={"include_usage": False}
    )
    return output


if "messages" not in st.session_state.keys():
    st.session_state.messages = []


def display():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])


# import clipboard

# def on_copy_click(text):
#     st.session_state.copied.append(text)
#     clipboard.copy(text)

def star_write():
    query = st.session_state.query
    key_point = st.session_state.key_point
    key_words = st.session_state.key_words
    writing_requirements = st.session_state.writing_requirements
    structured_data = parse_markdown('/data/wsx_workspace/gx_demos/ai_writer/docx_to_md.md')
    with st.chat_message("user"):
        st.session_state.messages.append(
            {"role": "user", "content": f"项目名称:{query},关键词:{key_words},项目要点:{key_point},写作要求:{writing_requirements}"})
        st.write(f"项目名称:{query},关键词:{key_words},项目要点:{key_point},写作要求:{writing_requirements}")
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = init_write(query, key_words, key_point, writing_requirements, structured_data)
            placeholder = st.empty()
            full_response = ''
            for output_stream in response:
                # result = ""
                if isinstance(output_stream, str):
                    full_response += output_stream
                else:
                    for chunk in output_stream:
                        chunk = chunk.choices
                        if chunk and chunk[0].delta.content:
                            full_response += chunk[0].delta.content
                            placeholder.markdown(full_response)
                    full_response += '\n'
            placeholder.markdown(full_response, unsafe_allow_html=True)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)
    display()


def polish():
    display()
    polish_requirements = st.session_state.polish_requirements
    selected_text = st.session_state.polish_target_content
    try:
        with st.chat_message("user"):
            st.session_state.messages.append(
                {"role": "user", "content": f"针对\n```text\n{selected_text}\n```\n进行润色，要求:{polish_requirements}"})
            st.write(f"针对\n```text\n{selected_text}\n```\n进行润色，要求:{polish_requirements}")
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                st_all_columns = st.columns(3)
                for draft_id in range(3):
                    column_subheader = f"草稿{draft_id + 1}:"
                    st_all_columns[draft_id].subheader(column_subheader)

                polish_result = rewrite_polish(selected_text, polish_requirements)
                polish_placeholder = [st_all_columns[0].empty(), st_all_columns[1].empty(), st_all_columns[2].empty()]
                polish_full_text = ['', '', '']
                choice_index = 0
                for chunk in polish_result:
                    chunk = chunk.choices
                    if chunk and chunk[0].delta.content is not None:
                        polish_full_text[choice_index % 3] += chunk[0].delta.content
                        polish_placeholder[0].markdown(polish_full_text[0], unsafe_allow_html=True)
                        polish_placeholder[1].markdown(polish_full_text[1], unsafe_allow_html=True)
                        polish_placeholder[2].markdown(polish_full_text[2], unsafe_allow_html=True)
                    choice_index += 1
        # message = {"role": "assistant", "content": polish_full_text[0]}
        st.session_state.messages.append({"role": "assistant", "content": '草稿1：\n' + polish_full_text[0]})
        st.session_state.messages.append({"role": "assistant", "content": '草稿2：\n' + polish_full_text[1]})
        st.session_state.messages.append({"role": "assistant", "content": '草稿3：\n' + polish_full_text[2]})
    except AttributeError:
        st.error("polish run error")


def expand():
    display()
    expand_requirements = st.session_state.expand_requirements
    selected_text = st.session_state.expand_target_content
    try:
        with st.chat_message("user"):
            st.session_state.messages.append(
                {"role": "user", "content": f"针对\n```text\n{selected_text}\n```\n进行扩写，要求:{expand_requirements}"})
            st.write(f"针对\n```text\n{selected_text}\n```\n进行扩写，要求:{expand_requirements}")
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                st_all_columns = st.columns(3)
                for draft_id in range(3):
                    column_subheader = f"草稿{draft_id + 1}:"
                    st_all_columns[draft_id].subheader(column_subheader)

                polish_result = rewrite_expand(selected_text, expand_requirements)
                polish_placeholder = [st_all_columns[0].empty(), st_all_columns[1].empty(), st_all_columns[2].empty()]
                polish_full_text = ['', '', '']
                choice_index = 0
                for chunk in polish_result:
                    chunk = chunk.choices
                    if chunk and chunk[0].delta.content is not None:
                        polish_full_text[choice_index % 3] += chunk[0].delta.content

                        polish_placeholder[0].markdown(polish_full_text[0], unsafe_allow_html=True)
                        polish_placeholder[1].markdown(polish_full_text[1], unsafe_allow_html=True)
                        polish_placeholder[2].markdown(polish_full_text[2], unsafe_allow_html=True)
                    choice_index += 1
            # st_all_columns[0].chat_message("assistant").write(polish_full_text)
            # st_all_columns[1].chat_message("assistant").write(polish_full_text_2)
            # message = {"role": "assistant", "content": polish_full_text}
            # st.session_state.messages.append(message)
        st.session_state.messages.append({"role": "assistant", "content": '草稿1：\n' + polish_full_text[0]})
        st.session_state.messages.append({"role": "assistant", "content": '草稿2：\n' + polish_full_text[1]})
        st.session_state.messages.append({"role": "assistant", "content": '草稿3：\n' + polish_full_text[2]})
    except AttributeError:
        st.error("expand run error")


def clear_chat_history():
    st.session_state.messages = []
    display()


import streamlit as st
import streamlit.components.v1 as components
import base64
import json
from io import BytesIO
from docx import Document


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
    b64 = base64.b64encode(object_to_download.getvalue()).decode()
    mime_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

    dl_link = f"""
    <html>
    <head>
    <title>Start Auto Download file</title>
    <script src="http://code.jquery.com/jquery-3.2.1.min.js"></script>
    <script>
    $('<a href="data:{mime_type};base64,{b64}" download="{download_filename}">')[0].click()
    </script>
    </head>
    </html>
    """
    return dl_link


def export():
    # 获取 Quill 编辑器中的文本
    edited_text = st.session_state.get("quill", "")

    # 创建一个新的 Word 文档
    doc = Document()

    # 将编辑器中的文本添加到文档中
    doc.add_paragraph(edited_text)

    # 创建一个字节流对象
    buffer = BytesIO()

    # 将文档保存到字节流
    doc.save(buffer)

    # 将字节流的当前位置移动到开始
    buffer.seek(0)

    components.html(
        download_button(buffer, 'output.docx'),
        height=0,
    )
    display()


with st.sidebar:
    st.title('✏️AI Writer')
    # st.subheader('Models and parameters')
    # temperature = st.sidebar.slider('temperature', min_value=0.01, max_value=5.0, value=0.1, step=0.01)
    # top_p = st.sidebar.slider('top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    # max_length = st.sidebar.slider('max_length', min_value=64, max_value=4096, value=512, step=8)

    with st.expander("⚙️写作设置", expanded=True):
        with st.form(key='writing_form'):
            use_ai_search = st.checkbox('是否使用AI搜索', value=True)
            st.text_area('项目标题', key='query')
            st.text_area('关键词', key='key_words')
            st.text_area('项目要点', key='key_point')
            st.text_area('写作要求', key='writing_requirements')

            st.form_submit_button('开始写作', on_click=star_write)

    with st.expander("📑润色", expanded=True):
        with st.form(key='polish_form'):
            st.text_area('需要润色的文本', key='polish_target_content')
            st.text_area('润色要求', key='polish_requirements')
            st.form_submit_button('开始润色', on_click=polish)

    with st.expander("🗒️扩写", expanded=True):
        with st.form(key='expand_form'):
            st.text_area('需要扩写的文本', key='expand_target_content')
            st.text_area('扩写要求', key='expand_requirements')
            st.form_submit_button('开始扩写', on_click=expand)

    st.button('Clear Chat History', on_click=clear_chat_history)

    # Streamlit 表单
    with st.form(key='edit_form'):
        edited_text = st_quill(key="quill", placeholder="在这里编辑文本...")
        st.form_submit_button('导出', on_click=export)
