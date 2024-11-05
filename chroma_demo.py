import json
from getpass import getuser

# from langchain_openai import OpenAIEmbeddings

import os.path
from getpass import getuser
from typing import Dict, Any, List

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_chroma import Chroma
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_ollama import OllamaEmbeddings
# Directory to persist the collection
from loguru import logger

from config import BASE_VECTOR_DB_DIR
from rag_document.rng_document import create_langchain_ollama_llm

# from langchain_openai import OpenAIEmbeddings

logger.info('current system user is {}', getuser())

if getuser() == 'zj':
    STATIC_URL = 'http://127.0.0.1:8501/app/static/'
    OLLAMA_BASE_URL = 'http://125.69.16.175:11434'
    PROJECT_DIR = '~/local-rag'
elif getuser() == 'ubuntu':
    STATIC_URL = 'http://125.69.16.175:8501/app/static/'
    OLLAMA_BASE_URL = 'http://125.69.16.175:11434'
elif getuser() == 'gx':
    STATIC_URL = 'http://127.0.0.1:8501/app/static/'
    OLLAMA_BASE_URL = 'http://125.69.16.175:11434'
    embedding_model='znbang/bge:large-zh-v1.5-f32'
else:
    STATIC_URL = 'http://192.168.1.159:8501/app/static/'
    OLLAMA_BASE_URL = 'http://192.168.1.159:11434'
# collection_name = 'laws_and_regulations'

print('OLLAMA_BASE_URL is {}'.format(OLLAMA_BASE_URL))

ollama_embeddings = OllamaEmbeddings(model=embedding_model, base_url=OLLAMA_BASE_URL)

llm = create_langchain_ollama_llm(
    model='qwen2.5:14b',
    base_url=OLLAMA_BASE_URL,
)

persist_directory = os.path.join('vector_db', 'alpaca_merge_medical_mechain')
vector_store = Chroma(
    collection_name='alpaca_merge_medical_mechain',
    embedding_function=ollama_embeddings,
    persist_directory=persist_directory,  # Where to save data locally, remove if not necessary
)
retriever = vector_store.as_retriever(search_kwargs={'k': 10})


# ###########################################  rag

system_prompt = (
    "你是一个负责文档分析专家。"
    "使用以下检索到的上下文来回答问题。"
    "如果你不知道答案，就说你不知道。"
    "你不能编造和上下文不符合的内容。"
    "\n\n"
    "{context}"
)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)


# question_answer_chain = create_stuff_documents_chain(llm, prompt)
# rag_chain = create_retrieval_chain(retriever, question_answer_chain)
# results = rag_chain.invoke({"input": "一次性使用医用外科口罩"})
#
# for res in results['context']:
#     print(f"* {res.page_content} [{res.metadata}]")
#     print(f"* [{res.metadata}]")
    # [{'filetype': 'docx', 'source': './static/pdf_and_doc/2024年医疗器械行业标准制修订计划项目.docx'}]
    #     [{'source': '{"image_path": "", "name": "经颅多普勒在线查看检测报告", "company": "南京科进有限公司", "image_url": ""}'}]

# ###########################################  手动构建



# ############################################## 相似度查询
results = vector_store.similarity_search_with_score(
    "正义堂祛红血丝护眼液",
    k=4,
    # filter={"source": 'image_path'}
    # filter={'source': '{"image_path": "", "name": "经颅多普勒在线查看检测报告", "company": "南京科进有限公司", "image_url": ""}'},
)
for res in results:
    res[0].metadata['content'] = ''
    res[0].metadata['image_url'] = ''
    print(f"* {res[1]} {res[0].page_content} [{res[0].metadata}]")
    # print(f"* [{res.metadata}]")
    # [{'filetype': 'docx', 'source': './static/pdf_and_doc/2024年医疗器械行业标准制修订计划项目.docx'}]
    #     [{'source': '{"image_path": "", "name": "经颅多普勒在线查看检测报告", "company": "南京科进有限公司", "image_url": ""}'}]




# ######################################################### do retrieval with contextual compression

# def pretty_print_docs(docs):
#     print(
#         f"\n{'-' * 100}\n".join(
#             [f"Document {i+1}:\n\n" + d.page_content for i, d in enumerate(docs)]
#         )
#     )
#
#
# from langchain.retrievers import ContextualCompressionRetriever
# from langchain.retrievers.document_compressors import LLMChainExtractor
#
#
# compressor = LLMChainExtractor.from_llm(llm)
# compression_retriever = ContextualCompressionRetriever(
#     base_compressor=compressor, base_retriever=retriever
# )
#
# compressed_docs = compression_retriever.invoke(
#     "口罩"
# )
# pretty_print_docs(compressed_docs)


# ####################################  MultiQueryRetriever
from langchain.retrievers.multi_query import MultiQueryRetriever
# import logging
#
# logging.basicConfig()
# logging.getLogger("langchain.retrievers.multi_query").setLevel(logging.DEBUG)
#
# question = "口罩"
#
# retriever_from_llm = MultiQueryRetriever.from_llm(
#     retriever=retriever, llm=llm
# )
# unique_docs = retriever_from_llm.invoke(question)
# len(unique_docs)

# ################ 手动构建 MultiQueryRetriever
# from typing import List
#
# from langchain_core.output_parsers import BaseOutputParser
# from langchain_core.prompts import PromptTemplate
#
#
# # Output parser will split the LLM result into a list of queries
# class LineListOutputParser(BaseOutputParser[List[str]]):
#     """Output parser for a list of lines."""
#
#     def parse(self, text: str) -> List[str]:
#         lines = text.strip().split("\n")
#         return list(filter(None, lines))  # Remove empty lines
#
#
# output_parser = LineListOutputParser()
#
# QUERY_PROMPT = PromptTemplate(
#     input_variables=["question"],
#     template="""You are an AI language model assistant. Your task is to generate five
#     different versions of the given user question to retrieve relevant documents from a vector
#     database. By generating multiple perspectives on the user question, your goal is to help
#     the user overcome some of the limitations of the distance-based similarity search.
#     Provide these alternative questions separated by newlines.
#     Original question: {question}""",
# )

# Chain
# llm_chain = QUERY_PROMPT | llm | output_parser

# Other inputs
# question = "口罩"
# Run
# retriever = MultiQueryRetriever(
#     retriever=retriever, llm_chain=llm_chain, parser_key="lines"
# )  # "lines" is the key (attribute name) of the parsed output
#
# # Results
# unique_docs = retriever.invoke("口罩")
# print(unique_docs)



from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
def rag_chat_stream(
        query: str,
        vector_store: Chroma,
        llm: ChatOllama
):
    """
    Args:
        input:
        vector_store:
        llm:
    Returns:
    """
    retriever = vector_store.as_retriever(search_kwargs={'k': 3})
    system_prompt = (
        "你是一个负责文档分析专家。"
        "使用以下检索到的上下文来回答问题。"
        "如果你不知道答案，就说你不知道。"
        "你不能编造和上下文不符合的内容。"
        "\n\n"
        "{context}"
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )

    # ########################################################  compression_retriever
    # 处理掉不相干的
    # compressor = LLMChainExtractor.from_llm(llm)
    # compression_retriever = ContextualCompressionRetriever(
    #     base_compressor=compressor, base_retriever=retriever
    # )
    # # 测试召回的文档
    # # compressed_docs = compression_retriever.invoke(query)
    # # manul_context = '\n\n'.join([doc.metadata['content'] for doc in compressed_docs])
    #
    # question_answer_chain = create_stuff_documents_chain(llm, prompt)
    # rag_chain = create_retrieval_chain(compression_retriever, question_answer_chain)
    #
    # # new retrieval
    # # manul_rag_chain = prompt | llm | StrOutputParser()
    # #
    # class CustomHandler(BaseCallbackHandler):
    #     def on_llm_start(
    #             self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    #     ) -> Any:
    #         formatted_prompts = "\n".join(prompts)
    #         # logger.info(f"Prompt:\n{formatted_prompts}")
    # # result = rag_chain.invoke({"input": query}, config={"callbacks": [CustomHandler()]})
    # # print(result)
    # for answer in rag_chain.stream({"input": query}, config={"callbacks": [CustomHandler()]}):
    #     yield answer


    # def format_docs(docs):
    #     net_content = "\n\n".join(doc.metadata['content'] for doc in compressed_docs)
    #     print(net_content)
    #     return net_content
    # rag_chain = (
    #     {"context": retriever | format_docs, "input": RunnablePassthrough()}
    #     | prompt
    #     | llm
    #     | StrOutputParser()
    # )
    # for chunk in rag_chain.stream("口罩"):
    #     print(chunk, end="", flush=True)


if __name__ == '__main__':
    query = '口罩 '
    # for trunk in rag_chat_stream(query, vector_store, llm):
    #     print(trunk)
