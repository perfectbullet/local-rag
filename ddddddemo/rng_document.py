import os
import os.path
from typing import Dict, List, Any
from uuid import uuid4
import langchain
from langchain_core.callbacks import BaseCallbackHandler
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_ollama import OllamaEmbeddings
# Directory to persist the collection
from langchain_text_splitters import RecursiveCharacterTextSplitter
from loguru import logger

langchain.verbose = True

BASE_VECTOR_DB_DIR = './vector_db'


def timer(func):
    """
    计算所用时间
    Args:
        func:

    Returns:

    """

    def func_wrapper(*args, **kwargs):
        from time import time
        time_start = time()
        result = func(*args, **kwargs)
        time_end = time()
        time_spend = time_end - time_start
        print('%s cost time: %.3f s' % (func.__name__, time_spend))
        return result

    return func_wrapper


def init_vectorstore(embeddings, documents):
    # embedding from documents object
    vectorstore = Chroma.from_documents(
        documents,
        embedding=embeddings,
        # embedding=OllamaEmbeddings(model='llama3', base_url='http://125.69.16.175:11434'),

    )
    return vectorstore


def init_vectorstore_basic(embeddings: OllamaEmbeddings, collection_name='chroma_langchain') -> Chroma:
    """
    Basic Initialization
    Args:
        embeddings:
        collection_name
        persist_directory  Where to save data locally, remove if not necessary
    Returns:

    """
    persist_directory = os.path.join(BASE_VECTOR_DB_DIR, collection_name)
    logger.info('persist_directory is {}', os.path.abspath(persist_directory))
    vector_store = Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=persist_directory,
    )
    return vector_store


def demo_add_document(vector_store: Chroma):
    document_1 = Document(
        page_content="I had chocolate chip pancakes and scrambled eggs for breakfast this morning.",
        metadata={"source": "tweet"},
        id=1,
    )

    document_2 = Document(
        page_content="The weather forecast for tomorrow is cloudy and overcast, with a high of 62 degrees.",
        metadata={"source": "news"},
        id=2,
    )

    document_3 = Document(
        page_content="Building an exciting new project with LangChain - come check it out!",
        metadata={"source": "tweet"},
        id=3,
    )

    document_4 = Document(
        page_content="Robbers broke into the city bank and stole $1 million in cash.",
        metadata={"source": "news"},
        id=4,
    )

    document_5 = Document(
        page_content="Wow! That was an amazing movie. I can't wait to see it again.",
        metadata={"source": "tweet"},
        id=5,
    )

    document_6 = Document(
        page_content="Is the new iPhone worth the price? Read this review to find out.",
        metadata={"source": "website"},
        id=6,
    )

    document_7 = Document(
        page_content="The top 10 soccer players in the world right now.",
        metadata={"source": "website"},
        id=7,
    )

    document_8 = Document(
        page_content="LangGraph is the best framework for building stateful, agentic applications!",
        metadata={"source": "tweet"},
        id=8,
    )

    document_9 = Document(
        page_content="The stock market is down 500 points today due to fears of a recession.",
        metadata={"source": "news"},
        id=9,
    )

    document_10 = Document(
        page_content="I have a bad feeling I am going to get deleted :(",
        metadata={"source": "tweet"},
        id=10,
    )

    documents = [
        document_1,
        document_2,
        document_3,
        document_4,
        document_5,
        document_6,
        document_7,
        document_8,
        document_9,
        document_10,
    ]
    uuids = [str(uuid4()) for _ in range(len(documents))]

    vector_store.add_documents(documents=documents, ids=uuids)


def query_vector_store(vector_store: Chroma, query: str, k=10, qfilter: Dict = None):
    """
    Args:
        vector_store:
        query:
        k: Number of results to return. Defaults to 4.
        qfilter:
    Returns:
    results = vector_store.similarity_search(
        "LangChain provides abstractions to make working with LLMs easy",
        k=4,
        filter={"source": "tweet"},
    )
    """
    results = vector_store.similarity_search_with_score(
        query, k=k, filter=qfilter
    )

    return results


@timer
def add_document(vector_store: Chroma, documents: List[Document]):
    """
    Args:
        vector_store:
        documents:
    Returns:
    """
    ids = vector_store.add_documents(documents)
    print('ids is {}, '.format(ids))
    return ids


def load_documents(doc_path: str):
    """
    load a document
    Args:
        doc_path:
    Returns:
    """
    # 加载Word文档并提取文本
    # loader = UnstructuredWordDocumentLoader("./short.docx")
    loader = Docx2txtLoader(doc_path)
    documents = loader.load()

    # 将文本分割成块
    # text_splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=500)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=100,
        length_function=len,
    )
    texts = text_splitter.split_documents(documents)
    return texts


def load_pdf(file_path):
    """
    Args:
        file_path:
    Returns:
    pip install "langchain-unstructured[local]"
    from langchain_unstructured import UnstructuredLoader
    file_paths = [
        "./example_data/layout-parser-paper.pdf",
        "./example_data/state_of_the_union.txt",
    ]
    loader = UnstructuredLoader(file_paths)
    https://python.langchain.com/docs/integrations/document_loaders/unstructured_file/
    """
    loader = UnstructuredPDFLoader(file_path)

    # 加载多个文档
    doc_splits = []
    logger.info("Loading raw document..., it may take long time " + loader.file_path)
    raw_documents = loader.load()
    logger.info("Splitting text...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    documents = text_splitter.split_documents(raw_documents)
    doc_splits.extend(documents)
    return doc_splits


def load_pdf_page(file_path):
    """
    load pdf per page
    Args:
        file_path:
    Returns:
    """
    logger.info('按页加载pdf')
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    return docs


def create_langchain_ollama_llm(
        model="qwen2.5:14b",
        base_url="http://125.69.16.175:11434",
) -> ChatOllama | None:
    """
    Create an instance of the Ollama language model.

    Parameters:
        - model (str): The name of the model to use for language processing.
        - base_url (str): The base URL for making API requests.
        - request_timeout (int, optional): The timeout for API requests in seconds. Defaults to 60.
    Returns:
        - llm: An instance of the Ollama language model with the specified configuration.
    """
    try:
        llm = ChatOllama(
            model=model,
            base_url=base_url,
            temperature=0,
            # other params...
        )
        return llm
    except Exception as e:
        logger.error(f"Error creating Ollama language model: {e}")
        return None


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
    retriever = vector_store.as_retriever()
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
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    class CustomHandler(BaseCallbackHandler):
        def on_llm_start(
                self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
        ) -> Any:
            formatted_prompts = "\n".join(prompts)
            # logger.info(f"Prompt:\n{formatted_prompts}")
    for answer in rag_chain.stream({"input": query}, config={"callbacks": [CustomHandler()]}):
        yield answer


def create_langchain_embedding_db(
        ollama_base_url='http://127.0.0.1:11434',
        embedding_model="znbang/bge:large-zh-v1.5-f32",
        collection_name=None
):
    """
    create ollama embedding db
    Args:
        collection_name:
        ollama_base_url:
        embedding_model:
    Returns:
    """
    if collection_name is None:
        collection_name = '{}-collection-v2'.format(embedding_model.replace(':', '_').replace('/', '_'))
    ollama_embeddings = OllamaEmbeddings(model=embedding_model, base_url=ollama_base_url)
    vector_store = init_vectorstore_basic(ollama_embeddings, collection_name, )
    return vector_store


def create_test_data():
    """
    文档向量化示例
    Returns:

    """
    demo_docx = './医疗器械经营质量管理规范.docx'
    demo_pdf = './机器学习常用数据集.pdf'
    vector_store = create_langchain_embedding_db()
    # for res, score in query_vector_store(vector_store, "Will it be hot tomorrow?", ):
    #     print(f"* [SIM={score:3f}] {res.page_content} [{res.metadata}]")
    res_text_splits = load_documents(demo_docx)
    ids = add_document(vector_store, res_text_splits)
    # for res, score in query_vector_store(vector_store, "医疗器械经营质量管理规范,职责与制度", ):
    #     print(f"* [SIM={score:3f}] {res.page_content[:10]} [{res.metadata}]")
    pdf_docs = load_pdf(demo_pdf)
    ids2 = add_document(vector_store, pdf_docs)
    # for res, score in query_vector_store(vector_store, "图像分类领域数据集"):
    #     print(f"* [SIM={score:3f}] {res.page_content[:100]} [{res.metadata}]")


def create_test_data2():
    """
    文档向量化示例2
    Returns:

    """
    # demo_docx = './医疗器械经营质量管理规范.docx'
    demo_pdf = './机器学习常用数据集.pdf'
    vector_store = create_langchain_embedding_db()
    # for res, score in query_vector_store(vector_store, "Will it be hot tomorrow?", ):
    #     print(f"* [SIM={score:3f}] {res.page_content} [{res.metadata}]")
    # res_text_splits = load_documents(demo_docx)
    # ids = add_document(vector_store, res_text_splits)
    # for res, score in query_vector_store(vector_store, "医疗器械经营质量管理规范,职责与制度", ):
    #     print(f"* [SIM={score:3f}] {res.page_content[:10]} [{res.metadata}]")
    # pdf_docs = load_pdf(demo_pdf)
    pdf_docs = load_pdf_page(demo_pdf)
    ids2 = add_document(vector_store, pdf_docs)
    # for res, score in query_vector_store(vector_store, "图像分类领域数据集"):
    #     print(f"* [SIM={score:3f}] {res.page_content[:100]} [{res.metadata}]")


def query_doc_demo():
    """
    文档查询示例
    Returns:
    """
    vector_store = create_langchain_embedding_db()
    llm = create_langchain_ollama_llm()
    q = "护眼液OEM"
    sources = []
    for chunk in rag_chat_stream(q, vector_store, llm):
        a = chunk.get('answer')
        if a:
            print(a, end='', flush=True)
        elif b := chunk.get('input'):
            pass
        elif c := chunk.get('context'):
            for doc in c:
                source = doc.metadata['source']
                sources.append(source)


if __name__ == '__main__':
    import os

    # os.environ["HTTP_PROXY"] = 'http://127.0.0.1:58591'
    # os.environ["HTTPS_PROXY"] = 'http://127.0.0.1:58591'
    os.environ["all_proxy"] = ''
    os.environ["ALL_PROXY"] = ''
    print('rag document start')
    create_test_data2()
