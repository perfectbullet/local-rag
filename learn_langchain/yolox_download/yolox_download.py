import os
# use proxy
os.environ["https_proxy"] = 'http://127.0.0.1:7897'
os.environ["http_proxy"] = 'http://127.0.0.1:7897'
os.environ["all_proxy"] = 'socks5://127.0.0.1:7897'

os.environ['CURL_CA_BUNDLE'] = ''

from langchain_unstructured import UnstructuredLoader
from langchain_community.document_loaders import PyPDFLoader

file_path = '''../split_pdf/merged_经济学百科.pdf'''


loader = UnstructuredLoader(
    file_path=file_path,
    # need yolo_x_layout under the unstructuredio
    strategy="hi_res",
    # partition_via_api=True,
    # coordinates=True,
    languages=['chi_sim',], # specific ocr languages
)
docs = []
print('start lazy load')
for doc in loader.lazy_load():
    docs.append(doc)
    print(doc)
print(docs)
