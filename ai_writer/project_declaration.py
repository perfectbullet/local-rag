import streamlit as st
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama
from loguru import logger


from initial_state import initial_state
from config import OLLAMA_BASE_URL
from export import export
from parse_markdown import parse_markdown

print('OLLAMA_BASE_URL is ', OLLAMA_BASE_URL)
llm = ChatOllama(
    model='qwen2.5:14b',
    base_url=OLLAMA_BASE_URL,
    temperature=0.6
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

    system = f"""## 角色描述：你是一名项目申报书写作专家，能根据项目主题和给定的文档模板的目录结构，生成完整的《项目申报书》。
## 工作流程
第一步：在开始撰写文章之前，必须认真阅读并牢记给定文档模板的目录结构。
第二步：使用Markdown格式，作为目申报书写作专家，撰写一篇完全详细的项目申报书，至少2000字。项目申报书应以严谨、追求事实的语气撰写。
必须阅读以下所有信息。

请使用{query}作为项目主题，并在每个标题下撰写至少100-500字的引人入胜的段落。
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


def display(st):
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


def start_write(st):
    with st.container(border=True):
        with st.container(border=True):
            query = st.session_state.query
            key_point = st.session_state.key_point
            key_words = st.session_state.key_words
            writing_requirements = st.session_state.writing_requirements
            structured_data = parse_markdown('project_declaration_template.md')
            st.markdown('''###### ✏️写作大纲和要求''')
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
                # st.session_state.full_response_placeholder = placeholder
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
                # display()


# def clear_chat_history():
#     st.session_state.messages = []
#     display()


def stop_generate(st):
    logger.info('stop generate')
    display(st)

def init_sdebar(st):
    with st.sidebar:
        with st.container(border=True):
            query_params = st.query_params
            print('query_params is {}'.format(query_params))
            # with st.expander("⚙️写作设置", expanded=True):
            #     with st.form(key='writing_form'):
            # use_ai_search = st.checkbox('是否使用AI搜索', value=False, available=False)
            st.text_area('**大纲标题**', value='医用压缩式雾化器申报书', key='query')
            st.text_area('**关键词**', value='医用超声雾化器，医疗器械分类目录，主机、雾化杯、连接管、吸入面罩', key='key_words')
            st.text_area('**大纲要点**',
                         value='1.医用压缩式雾化器工作原理：医用压缩式雾化器应用的是文丘里效应原理，一般是通过气体压缩机产生的压缩气体为驱动源来产生及传输气雾的，其工作原理：压缩机产生的压缩空气从喷嘴喷出时，通过喷嘴与吸水管之间产生的负压作用，向上吸起药液。吸上来的药液冲击到上方的隔片，变成极细的雾状向外部喷出。\n'
                               '2.试验结果作为多功能数据采集终端_手持式EDAT-A2的环境适应性依据之一。'
                               '3.医用超声雾化器一般由主机、雾化杯、连接管、咬嘴或吸入面罩组成，其中的主机一般由超声波发生器(超声换能器)、超声薄膜、送风装置、调节和控制系统组成',
                         key='key_point')
            st.text_area('**写作要求**', value="", key='writing_requirements')

            with open('ai_writer_css.css', mode='rt', encoding='utf-8') as f:
                writer_css = f.read()
                # 修改页面布局
                st.markdown(writer_css, unsafe_allow_html=True)
            col_v1, col_v2, col_v3 = st.columns([1, 1, 1])
            with col_v1:
                if st.button('**生成**'):
                    st.session_state.start_write = True
                    st.session_state.stop_generate = False
                    st.session_state.start_export = False

            with col_v2:
                if st.button('**停止**'):
                    st.session_state.stop_generate = True
                    st.session_state.start_write = False
                    st.session_state.start_export = False

            with col_v3:
                if st.button('**导出**'):
                    st.session_state.start_export = True
                    st.session_state.start_write = False
                    st.session_state.stop_generate = False


def start_three(st):
    if st.session_state.start_write:
        start_write(st)
    if st.session_state.stop_generate:
        stop_generate(st)
    if st.session_state.start_export:
        export(st)
        stop_generate(st)

initial_state(st)
init_sdebar(st)

start_three(st)
