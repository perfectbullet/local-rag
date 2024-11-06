from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders import UnstructuredWordDocumentLoader

def simple_loader():
    loader = Docx2txtLoader("./demo_exp_report.docx")

    data = loader.load()

    print(data)
    # len of data is 1


def unstructured_loader():


    # loader = Docx2txtLoader("./demo_exp_report.docx")

    # Retain Elements
    loader = UnstructuredWordDocumentLoader("./demo_exp_report.docx", mode="elements")

    datas = loader.load()
    categorys = set()
    for data in datas:
        page_content = data.page_content
        if '工作结束时间' in page_content:
            pass
        print('*' * 100)
        print(data.metadata['category'])
        categorys.add(data.metadata['category'])
        print(data.page_content)
    print(categorys)


if __name__ == "__main__":
    unstructured_loader()
