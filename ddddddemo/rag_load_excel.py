import json
from typing import Tuple, List

import pandas as pd
from langchain_core.documents import Document

from deal_excel_and_json import read_json

from ddddddemo.rng_document import create_langchain_embedding_db, add_document, query_vector_store


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
    file_name = 'ddddddemo/oktest_image_url_local_image.json'
    recovered_json = read_json(file_name)
    vector_store = create_langchain_embedding_db(collection_name='oktest_image_url_local_image')
    doc_list = []
    for data in recovered_json:
        metadata = {
            'image_path': data.get('image_path', ''),
            'name': data['item_name'],
            'company': data['item_name'],
            'image_url': data['image_url']
        }
        doc = Document(
            page_content='```{}```\n\n{}'.format(data['item_name'], data['content']),
            metadata={"source": json.dumps(metadata, ensure_ascii=False)},
        )
        doc_list.append(doc)
    print('len of doc_list ', len(doc_list))
    # print('doc_list is {}'.format(doc_list[:3]))
    ids = add_document(vector_store, doc_list)
    # 正义堂祛红血丝护眼液OEM贴牌代工
    # 三申卧式圆形压力蒸汽灭菌器YX450W双温度显示和控制
    for res, score in query_vector_store(vector_store, "高频电刀", ):
        print(f"* [SIM={score:3f}]  [{res.metadata}]")


if __name__ == '__main__':
    add_data_from_json()
