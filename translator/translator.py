import os
import sys
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

os.environ["HTTP_PROXY"] = ''
os.environ["HTTPS_PROXY"] = ''
os.environ["all_proxy"] = ''
os.environ["ALL_PROXY"] = ''

username = os.environ.get('USERNAME')
sys_name = sys.platform
print(username, sys_name)

if sys_name == 'win32' and username == 'gx':
    model = OllamaLLM(model="qwen2.5:14b", base_url='http://127.0.0.1:11434')


sys_prompt = """现在你是一个军事领域的英汉翻译器，把给定文本翻译成中文。
翻译句子和段落时，要注意联系上下文，武器专有名称不用翻译。
你以军事解说的语言风格来翻译。
"""
#
# """你是一位精通简体中文的专业翻译，曾参与《纽约时报》和《经济学人》中文版的翻译工作，因此对于新闻和时事文章的翻译有深入的理解。我希望你能帮我将以下英文新闻段落翻译成中文，风格与上述杂志的中文版相似。
#
# 规则：
# - 翻译时要准确传达新闻事实和背景。
# - 保留特定的英文术语或名字，并在其前后加上空格，例如："中 UN 文"。
# - 分成两次翻译，并且打印每一次结果：
# 1. 根据新闻内容直译，不要遗漏任何信息
# 2. 根据第一次直译的结果重新意译，遵守原意的前提下让内容更通俗易懂，符合中文表达习惯
#
# 本条消息只需要回复OK，接下来的消息我将会给你发送完整内容，收到后请按照上面的规则打印两次翻译结果。"""


new_root = 'D:\zj_work\兵棋推演DB\Descriptions-translation'

trans_files = os.listdir(new_root)

for root, dirs,  files in os.walk('D:\zj_work\兵棋推演DB\Descriptions'):
    for name in files:
        if name in trans_files:
            print(f'skip {name}')
            continue
        with open(os.path.join(root, name), 'rt', encoding='utf8') as f:
            content = f.read()
            prompt = ChatPromptTemplate.from_messages([
                ('system', sys_prompt),
                ('user', '{content}')
            ])
            chain = prompt | model
            res = chain.invoke({"content": content})
        with open(os.path.join(new_root, name), 'wt', encoding='utf8') as f:
            f.write(res)
            print(f'save {name} finished')
