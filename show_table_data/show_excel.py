import pandas as pd
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate

from utils.langchain_rag_for_st import langchain_chat_stream, get_langchain_ollama_llm
from langchain_core.output_parsers import StrOutputParser



def st_show_excel(input: str, excel_path:str, st):
    # build a show excel chain
    system_prompt = (
        "你是一个AI助手。"
        "简单回答用户提问就好。"
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )
    # print('prompt is {}'.format(prompt))
    ollama_endpoint = st.session_state["ollama_endpoint"]
    selected_model = st.session_state["selected_model"]
    llm = get_langchain_ollama_llm(base_url=ollama_endpoint, model=selected_model)

    parser = StrOutputParser()
    rag_chain = prompt | llm | parser
    output_placeholder = st.empty()

    response = ""

    for trunk in rag_chain.stream({"input": input}):
        response += trunk
        output_placeholder.markdown(response)
    df = pd.read_excel(excel_path)
    datas = df.fillna('')
    st.table(datas)
    return response