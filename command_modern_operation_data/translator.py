import os
import re
import json

from langchain_core.prompts import ChatPromptTemplate

from langchain_models.ollama_models import model

new_root = 'D:\zj_work\兵棋推演DB\Descriptions-json-zh'
os.makedirs(new_root, exist_ok=True)
json_files = os.listdir(new_root)
keys = set()
# 种类
device_set = set()
sys_prompt = """现在你是一个军事领域的英汉翻译器，把给定文本翻译成中文。
翻译句子和段落时，要注意联系上下文，武器专有名称不用翻译。
你以军事解说的语言风格来翻译。
"""


for root, dirs,  files in os.walk('D:\zj_work\兵棋推演DB\Descriptions'):
    # files.reverse()
    for name in files:
        print(f'deal {name} to json')
        device_set.add(name.split('_')[0])
        base_dir_name = os.path.basename(root)
        new_dir = os.path.join(new_root, base_dir_name)
        os.makedirs(new_dir, exist_ok=True)
        new_json_path = os.path.join(new_dir, name.replace('.txt', '.json'))
        if os.path.exists(new_json_path):
            print(f'skip {name}')
            continue

        with open(os.path.join(root, name), 'rb') as f:
            # content = f.read().decode(encoding='UTF-8', errors='ignore')
            print('*' * 100)
            content = ''
            res = {}
            key = None
            for line in f:
                # print(content)
                line_str = line.decode(encoding='UTF-8', errors='ignore')
                line_str = line_str.strip()
                mt = re.match(r'(^[A-Z]+):(.*)', line_str)
                if mt is not None:
                    key = mt.group(1)
                    keys.add(key)
                    res[key] = mt.group(2).strip()
                elif key is not None and not line_str == '\n':
                    res[key] += line_str
                else:
                    pass
            if res:
                for key in res:
                    prompt = ChatPromptTemplate.from_messages([
                        ('system', sys_prompt),
                        ('user', '{content}')
                    ])
                    chain = prompt | model
                    translation_text = chain.invoke({"content": res[key]})
                    res[key] = translation_text

                res_json = json.dumps(res, indent=4, ensure_ascii=False)
                print(res_json)

                with open(new_json_path, 'wt', encoding='utf8') as f:
                    f.write(res_json)
                    print(f'save {name} finished')
print(keys)
print(device_set)
