import json
from typing import Tuple, List

import pandas as pd
from langchain_core.documents import Document

from deal_excel_and_json import read_json

try:
    from ddddddemo.rng_document import create_langchain_embedding_db, add_document, query_vector_store
except:
    from rng_document import create_langchain_embedding_db, add_document, query_vector_store


def read_excel(excel_file) -> Tuple[List, List]:
    datas = pd.read_excel(excel_file)
    datas = datas.fillna('')
    headers = list(datas)
    recovered_json = []
    for data in datas.to_dict('records'):
        recovered_json.append(data)
    return headers, recovered_json


def add_data_from_excel():
    file_name = 'ddddddemo/alpaca_merge-医疗器械-产品详细v2-test.xlsx'
    headers, recovered_json = read_excel(file_name)

    vector_store = create_langchain_embedding_db()

    doc_list = []
    for data in recovered_json:
        doc = Document(
            page_content=data['output'],
            metadata={"source": "{}, row {}".format(file_name, data['instruction'])},
        )
        doc_list.append(doc)
    print('len of doc_list ', len(doc_list))
    # print('doc_list is {}'.format(doc_list[:3]))
    ids = add_document(vector_store, doc_list)
    # 正义堂祛红血丝护眼液OEM贴牌代工
    # 三申卧式圆形压力蒸汽灭菌器YX450W双温度显示和控制
    for res, score in query_vector_store(vector_store, "护眼液OEM", ):
        print(f"* [SIM={score:3f}] {res.page_content[:100]} [{res.metadata}]")


def add_data_from_json():
    """
    按 sft数据集向量化示例
    Returns:

    """
    collection_name = 'alpaca_merge_medical_mechain'
    # ollama_base_url = 'http://125.69.16.175:11434'
    ollama_base_url = ''
    file_name = 'ddddddemo/oktest_image_url_local_image.json'
    recovered_json = read_json(file_name)
    vector_store = create_langchain_embedding_db(
        ollama_base_url=ollama_base_url,
        embedding_model="znbang/bge:large-zh-v1.5-f32",
        collection_name=collection_name
    )
    doc_list = []
    seen_urls = set()
    for data in recovered_json:
        if data['url'] in seen_urls:
            continue
        metadata = {
            'image_path': data.get('image_path', ''),
            'name': data['item_name'],
            'company': data['item_name'],
            'image_url': data['image_url']
        }
        seen_urls.add(data['url'])
        doc = Document(
            page_content='{}'.format(data['content']),
            metadata={"source": json.dumps(metadata, ensure_ascii=False)},
        )
        doc_list.append(doc)
    print('len of doc_list ', len(doc_list))
    print('doc_list is {}'.format(doc_list[:3]))

    step = 50
    l = len(doc_list)
    doc_list_slice = [doc_list[i:i + step] for i in range(0, l, step)]
    for lslice in doc_list_slice:
        ids = add_document(vector_store, lslice)
    # 正义堂祛红血丝护眼液OEM贴牌代工
    # 三申卧式圆形压力蒸汽灭菌器YX450W双温度显示和控制
    for res, score in query_vector_store(vector_store, "脂肪吸引器", ):
        print(f"* [SIM={score:3f}]  [{res.metadata}]")


if __name__ == '__main__':
    add_data_from_json()
