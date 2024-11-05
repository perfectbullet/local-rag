from langchain_community.document_loaders import Docx2txtLoader

loader = Docx2txtLoader("./demo_exp_report.doc")

data = loader.load()

print(data)