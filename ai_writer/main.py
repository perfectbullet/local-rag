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
from export import export
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





def clear_chat_history():
    st.session_state.messages = []
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
        if st.button('**导出**', on_click=export):
            display()

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
