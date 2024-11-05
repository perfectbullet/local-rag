from langchain_chroma import Chroma
# from langchain_openai import OpenAIEmbeddings
from langchain_ollama import OllamaEmbeddings

from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.document_loaders import UnstructuredWordDocumentLoader
import os
from langchain_ollama import ChatOllama

from langchain_ollama import OllamaEmbeddings


model = ChatOllama(
    model="llama3.1",
    # model="qwen2.5:14b",
    # temperature=0,
    # other params...
)

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = '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'
filename = "./data_test/医疗器械经营质量管理规范.docx"
# loader = UnstructuredWordDocumentLoader(filename, mode="elements")
loader = UnstructuredWordDocumentLoader(filename)
docs = loader.load()


text_splitter = RecursiveCharacterTextSplitter(
    # chunk_size=1000, chunk_overlap=200, add_start_index=True
    chunk_size=500, chunk_overlap=100, add_start_index=True
)
all_splits = text_splitter.split_documents(docs)


from langchain_chroma import Chroma
# from langchain_openai import OpenAIEmbeddings
from langchain_ollama import OllamaEmbeddings

vectorstore = Chroma.from_documents(documents=all_splits, embedding=OllamaEmbeddings(model="llama3.1"))

retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 6})

retrieved_docs = retriever.invoke("医疗器械经营质量管理规范是什么？")


# 检索和生成：生成
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

system_prompt = (
    "您是问答任务的助手。 使用以下检索到的上下文来回答问题。 如果您不知道答案，请说您不知道。 最多使用三句话并保持答案简洁。\n\n {context}"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)


question_answer_chain = create_stuff_documents_chain(model, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

response = rag_chain.invoke({"input": "医疗器械经营质量管理规范有几条要求"})
print(response["answer"])
