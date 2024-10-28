import base64
import re
from collections import defaultdict

import streamlit as st
import streamlit.components.v1 as components
from Markdown2docx import Markdown2docx
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama
from loguru import logger
# from streamlit_quill import st_quill

from config import OLLAMA_BASE_URL

print('OLLAMA_BASE_URL is ', OLLAMA_BASE_URL)
llm = ChatOllama(
    model='qwen2.5:14b',
    base_url=OLLAMA_BASE_URL,
    temperature=0.7
)

st.set_page_config(
    page_title="文案创作",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state='expanded',
)


def parse_markdown(md_filepath):
    markdown_text = ''
    with open(md_filepath, 'r', encoding='utf8') as f:
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
    logger.info('structured_data is {}', structured_data)
    return structured_data


# Function for generating llm response
def init_write(query, key_words, key_point, writing_requirements, structured_data):
    toc = []
    for h1, h2_data in structured_data.items():
        toc.append(h1)
        if not isinstance(h2_data, str):
            for h2, content in h2_data.items():
                toc.append(h2)
    toc = '\n'.join(toc)

    system = f"""## 角色描述：你是一名试验大纲写作专家，能根据项目主题和给定的文档模板的目录结构，生成完整的《试验大纲》。
## 工作流程
第一步：在开始撰写文章之前，必须认真阅读并牢记给定文档模板的目录结构。
第二步：使用Markdown格式，作为专家文章作者，撰写一篇完全详细、长篇、100%独特、创意且人性化的信息性文章，至少2000字。文章应以严谨、追求事实的语气撰写。
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
            messages = [
                SystemMessage(content=system),
                HumanMessage(content=user),
            ]

            parser = StrOutputParser()

            chain = llm | parser
            stream_res = chain.stream(messages)
            all_outputs.append(stream_res)
        else:
            for h2, content in h2_data.items():
                user = f"""请开始写二级章节`{h1}`的三级小章节`{h2}`。我为你准备了一些可供参考的内容来辅助你写作。你可以参考其中的篇章分布和语言风格。
供参考的内容如下:
```text
{content}
```
## 注意：如果供参考的内容与项目主题和项目关键词等不相关，请不必参考，自行编写。

请以`## {h2}`为开头，输出写作的内容。
"""
                messages = [
                    SystemMessage(content=system),
                    HumanMessage(content=user),
                ]

                parser = StrOutputParser()

                chain = llm | parser
                stream_res = chain.stream(messages)
                all_outputs.append(stream_res)

    return all_outputs


def rewrite_polish(selected_text, polish_requirements):
    system = """## 角色描述：你是一名项目写作专家，擅长对项目申请书中的文字进行润色。
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

    messages = [
        SystemMessage(content=system),
        HumanMessage(content=user),
    ]

    parser = StrOutputParser()

    chain = llm | parser
    stream_res = chain.stream(messages)
    # all_outputs.append(stream_res)
    return stream_res


def rewrite_expand(selected_text, polish_requirements):
    system = """## 角色描述：你是一名项目写作专家，擅长对项目申请书中的文字进行扩写。
## 工作流程
第一步：在开始扩写之前，必须认真阅读并牢记扩写的要点。
第二步：使用Markdown格式，按照扩写的要求，对给你的文字进行扩写。"""
    user = f"""
原文字如下:
{selected_text}
扩写的要点如下:
{polish_requirements}"""

    messages = [
        SystemMessage(content=system),
        HumanMessage(content=user),
    ]

    parser = StrOutputParser()

    chain = llm | parser
    stream_res = chain.stream(messages)

    return stream_res


if "messages" not in st.session_state.keys():
    st.session_state.messages = []


def display():
    logger.info('display')
    with st.container(border=True):
        with st.container(border=True):
            st.markdown('''###### ✏️写作大纲和要求''')
            with st.container(border=True):
                placeholder = st.empty()
                placeholder.markdown(st.session_state.write_requirement)
            st.markdown('''###### ✏️文案生成''')
            with st.container(border=True):
                if st.session_state.full_response:
                    st.write(st.session_state.full_response)


def start_write():
    # col1, = st.columns([1, ])
    with st.container(border=True):
        with st.container(border=True):
            query = st.session_state.query
            key_point = st.session_state.key_point
            key_words = st.session_state.key_words
            writing_requirements = st.session_state.writing_requirements
            structured_data = parse_markdown('docx_to_md.md')
            st.markdown('''###### 🗨写作大纲和要求''')
            with st.container(border=True):
                st.session_state.messages.append(
                    {"role": "user",
                     "content": f"大纲名称:{query},关键词:{key_words},大纲要点:{key_point},写作要求:{writing_requirements}"})
                write_requirement = f"大纲名称:{query}\n\n关键词: {key_words}\n\n大纲要点:{key_point}\n\n写作要求:{writing_requirements}"
                st.session_state.write_requirement = write_requirement
                placeholder = st.empty()
                placeholder.markdown(write_requirement)

            st.markdown('''###### ✏️文案生成''')
            with st.container(border=True):
                response = init_write(query, key_words, key_point, writing_requirements, structured_data)
                st.session_state.stop_generate = False
                placeholder = st.empty()
                st.session_state.full_response_placeholder = placeholder
                full_response = ''
                placeholder.markdown(full_response)
                for output_stream in response:

                    if st.session_state.stop_generate:
                        placeholder.markdown(full_response)
                        break
                    if isinstance(output_stream, str):
                        full_response += output_stream
                    else:
                        for chunk in output_stream:
                            full_response += chunk
                            placeholder.markdown(full_response)
                            st.session_state.full_response = full_response
                        full_response += '\n'
                placeholder.markdown(full_response, unsafe_allow_html=True)
                message = {"role": "assistant", "content": full_response}
                print('full_response is {}'.format(full_response))
                st.session_state.messages.append(message)
                display()


def polish():
    display()
    polish_requirements = st.session_state.polish_requirements
    selected_text = st.session_state.polish_target_content
    try:
        with st.chat_message("user"):
            st.session_state.messages.append(
                {"role": "user",
                 "content": f"针对\n```text\n{selected_text}\n```\n进行润色，要求:{polish_requirements}"})
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
                {"role": "user",
                 "content": f"针对\n```text\n{selected_text}\n```\n进行扩写，要求:{expand_requirements}"})
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
        st.session_state.messages.append({"role": "assistant", "content": '草稿1：\n' + polish_full_text[0]})
        st.session_state.messages.append({"role": "assistant", "content": '草稿2：\n' + polish_full_text[1]})
        st.session_state.messages.append({"role": "assistant", "content": '草稿3：\n' + polish_full_text[2]})
    except AttributeError:
        st.error("expand run error")


def clear_chat_history():
    st.session_state.messages = []
    display()


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
        # <script src="http://code.jquery.com/jquery-3.2.1.min.js"></script>
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


def export():
    # 获取 Quill 编辑器中的文本
    # edited_text = st.session_state.get("quill", "")
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
    display()


if "full_response" not in st.session_state:
    st.session_state.full_response = ''
if "messages" not in st.session_state:
    st.session_state.messages = []
if "write_requirement" not in st.session_state:
    st.session_state.write_requirement = ''
# if "query" not in st.session_state:
#     st.session_state.query = ""
# if "key_point" not in st.session_state:
#     st.session_state.key_point = ""
# if "key_words" not in st.session_state:
#     st.session_state.key_words = ""
# if "writing_requirements" not in st.session_state:
#     st.session_state.writing_requirements = ""
if "polish_target_content" not in st.session_state:
    st.session_state.polish_target_content = ""
if "polish_requirements" not in st.session_state:
    st.session_state.polish_requirements = ""
if "expand_target_content" not in st.session_state:
    st.session_state.expand_target_content = ""
if "expand_requirements" not in st.session_state:
    st.session_state.expand_requirements = ""
if "stop_generate" not in st.session_state:
    st.session_state.stop_generate = False


def export_to_buffer():
    latest_message = st.session_state.full_response
    logger.info('latest_message is {}'.format(latest_message))
    project = Markdown2docx('tmp1215')
    project.eat_soup()
    project.save()
    logger.info('export_to_buffer tmp1215 is done')
    with open('tmp1215.docx', mode='rb') as f:
        return f.read()


def stop_generate():
    st.session_state.stop_generate = True
    display()


with st.sidebar:
    query_params = st.query_params
    print('query_params is {}'.format(query_params))
    st.markdown('#### 文案创作')
    # with st.expander("⚙️写作设置", expanded=True):
    #     with st.form(key='writing_form'):
    # use_ai_search = st.checkbox('是否使用AI搜索', value=False, available=False)
    st.text_area('**大纲标题**', value='多功能数据采集终端手持式试验大纲', key='query')
    st.text_area('**关键词**', value='振动试验，低温贮存，低温工作，高温贮存，高温工作，自由跌落', key='key_words')
    st.text_area('**大纲要点**',
                 value='1.本设计试验大纲的试验目的是验证多功能数据采集终端手持式EDAT-A2的物理特性、功能和性能、环境适应性、耐久性和可靠性。\n2.试验结果作为多功能数据采集终端_手持式EDAT-A2的环境适应性依据之一。',
                 key='key_point')
    st.text_area('**写作要求**', value="", key='writing_requirements')
    col_v1, col_v2, col_v3 = st.columns([1, 1, 1])
    with col_v1:
        st.button('**生成**', on_click=start_write)
    with col_v2:
        st.button('**停止**', on_click=stop_generate)
    with col_v3:
        st.button('**导出**', on_click=export)

    # 修改页面布局
    st.markdown(
        r"""
    <style>
    header[data-testid='stHeader'] {
       visibility: hidden;
    }
    header[data-testid='stHeader'] {
      display:none;
    }
    .st-emotion-cache-1jicfl2{
        padding:0px 0rem;
    }
     hr{
        margin:0;
    }
    div[data-testid = "stSidebarHeader"]{
         background: url("/app/static/logo.png") no-repeat;
     }
    button[data-testid="stBaseButton-secondary"]{
        padding: 0.25rem 1rem;
    }
    div[data-testid="stMarkdownContainer"] > h4{
       border-bottom: 1px solid #d0e1e0;
        border-block-width: 3px;
        margin-bottom: 8px;
    }
    h2{
        padding: 0rem 0px;
        line-height: 1;
    }
    section[data-testid="stFileUploaderDropzone" ]{
        align-items: center !important;
    }
    
label[data-testid="stWidgetLabel"]{
	width:80px;
}
    section[data-testid="stSidebar"]{
        border-right: 1px solid #1ba2a0;
        background-color: rgb(236 245 245);
    }

    textarea[type="textarea"]{
       border: 1px solid #eee;
        border-radius: 10px;
        background: white;
    }
    div[data-testid="stSidebarUserContent"]{
            padding: 0px 1rem 0rem;
    }
    .stTextArea{
        display:flex;
    }
    .st-b6{
        font-size: 14px;
    }
    h1,h2,h3,h4 {
        font-size: 14px;
    }
    p,h6{
        font-size: 14px;
    }
    button[data-testid="baseButton-secondary"]{
       display: inline-flex;
        -webkit-box-align: center;
        align-items: center;
        -webkit-box-pack: center;
        justify-content: center;
        padding: 0.25rem 1.75rem;
        border-radius: 0.5rem;
        min-height: 2rem;
        margin: 0px;
        line-height: 1;
        width: auto;
        user-select: none;
        background-color: rgb(27 162 160);
        border: 1px solid rgba(49, 51, 63, 0.2);
        color: white;
        font-size: 14px;
        font-weight: normal;
    }
    button[data-testid="baseButton-secondary"]:hover{
      border:1px solid blue;
     color:yellow;	
    }
    
    button[data-testid="baseButton-secondary"]:active{
          color: yellow;
        border-color: #cde709;
        background-color: rgb(27 162 160);
    }
    
    div[class^='st-emotion-cache']{
        opacity:1 !important;
    }
    
    div[data-testid="element-container"]{
        opacity:1;
    }
    button[data-testid="baseButton-secondary"]:focus:not(:active) {
        border:1px solid blue;
     color:yellow;	
    }
    button[class^='st-emotion-cache']:focus:not(:active){
         border:1px solid blue;
     color:yellow;	
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:first-child{
        border:none;
    }
    section.main > div.block-container  > div > div > div > div > div > div > div > div > div > div:nth-child(2) {
       background: #ecf5f5;
    }
    section.main{
            border-right: 1px solid #40b7b5;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )
