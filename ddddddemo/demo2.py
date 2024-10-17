from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.llms import OpenAI

from langchain_community.llms.chatglm3 import ChatGLM3

from langchain_community.document_loaders import Docx2txtLoader
from langchain_core.output_parsers import JsonOutputParser
from operator import itemgetter
from langchain_core.messages import AIMessage, HumanMessage, get_buffer_string
from langchain_core.prompts import format_document
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_openai.chat_models import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.prompts.prompt import PromptTemplate
from langchain.prompts.chat import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain.memory import ConversationBufferMemory
import langchain.tools
from flask import Flask


need_embedding = False

persist_directory = 'chroma'
if need_embedding:
    # 加载Word文档并提取文本
    # loader = UnstructuredWordDocumentLoader("./short.docx")
    loader = Docx2txtLoader("./short.docx")
    documents = loader.load()

    # 将文本分割成块
    text_splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=500)
    texts = text_splitter.split_documents(documents)

    # 初始化向量存储和嵌入
    # embeddings = OpenAIEmbeddings()
    embeddings = HuggingFaceEmbeddings(model_name='./text2vec-base-chinese')
    db = Chroma.from_documents(texts, embeddings, persist_directory=persist_directory)
    # 保存向量存储
    db.persist()
else:
    # 加载向量存储
    # embeddings = OpenAIEmbeddings()
    embeddings = HuggingFaceEmbeddings(model_name='./text2vec-base-chinese')
    db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)

# 定义检索器和生成器
retriever = db.as_retriever()

# qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=retriever)
#
# # 处理用户查询
# query = "全息智能感知"
# result = qa.run(query)
# print(result)

# =====================================
_template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question, in its orignal language.

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""
CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template)

template = """Answer the question based only on the following context, 请用中文回复:
{context}

Question: {question}
"""
ANSWER_PROMPT = ChatPromptTemplate.from_template(template)
DEFAULT_DOCUMENT_PROMPT = PromptTemplate.from_template(template="{page_content}")


def llm():
    result = ChatOpenAI(temperature=0.8)
    # endpoint_url = "http://10.10.7.160:8000/v1/chat/completions"
    # result = ChatGLM3(
    #     endpoint_url=endpoint_url,
    #     max_tokens=2048,
    # )
    return result


def _combine_documents(
    docs, document_prompt=DEFAULT_DOCUMENT_PROMPT, document_separator="\n\n"
):
    doc_strings = [format_document(doc, document_prompt) for doc in docs]
    return document_separator.join(doc_strings)


_inputs = RunnableParallel(
    standalone_question=RunnablePassthrough.assign(
        chat_history=lambda x: get_buffer_string(x["chat_history"])
    )
    | CONDENSE_QUESTION_PROMPT
    | llm()
    | StrOutputParser(),
)

memory = ConversationBufferMemory(
    return_messages=True, output_key="answer", input_key="question"
)

# First we add a step to load memory
# This adds a "memory" key to the input object
loaded_memory = RunnablePassthrough.assign(
    chat_history=RunnableLambda(memory.load_memory_variables) | itemgetter("history"),
)
# Now we calculate the standalone question
standalone_question = {
    "standalone_question": {
        "question": lambda x: x["question"],
        "chat_history": lambda x: get_buffer_string(x["chat_history"]),
    }
    | CONDENSE_QUESTION_PROMPT
    | llm()
    | StrOutputParser(),
}
# Now we retrieve the documents
retrieved_documents = {
    "docs": itemgetter("standalone_question") | retriever,
    "question": lambda x: x["standalone_question"],
}
# Now we construct the inputs for the final prompt
final_inputs = {
    "context": lambda x: _combine_documents(x["docs"]),
    "question": itemgetter("question"),
}
# And finally, we do the part that returns the answers
answer = {
    "answer": final_inputs | ANSWER_PROMPT | llm(),
    "docs": itemgetter("docs"),
}
# And now we put it all together!
final_chain = loaded_memory | standalone_question | retrieved_documents | answer


# flask
app = Flask(__name__)


@app.route("/get/<question>")
def get(question):
    inputs = {"question": f"{question}"}
    result = final_chain.invoke(inputs)
    # print("=============================")
    print(f"result1: {result}")
    return str(result['answer'])


app.run(host='0.0.0.0', port=8888, debug=True)

