import os
import re
import sys
from os.path import join, getsize
from typing import List, Tuple

import pandas as pd

def read_excel(excel_file) -> Tuple[List, List]:
    datas = pd.read_excel(excel_file)
    datas = datas.fillna('')
    headers = list(datas)
    recovered_json = []
    for data in datas.to_dict('records'):
        recovered_json.append(data)
    return headers, recovered_json


def find_files(data_dir, extension='.xlsx') -> List:
    ok_files = []
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.endswith(extension):
                file_path = os.path.join(root, file)
                print(file_path)
                ok_files.append(file_path)
    return ok_files

if __name__ == '__main__':
    ep = '../爬虫全部数据20241014/产品信息/医疗器械-产品详细-好的原始数据.xlsx'
    read_excel(ep)
