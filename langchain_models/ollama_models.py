import os
import sys
from langchain_ollama.llms import OllamaLLM


os.environ["HTTP_PROXY"] = ''
os.environ["HTTPS_PROXY"] = ''
os.environ["all_proxy"] = ''
os.environ["ALL_PROXY"] = ''

username = os.environ.get('USERNAME')
sys_name = sys.platform
print(username, sys_name)

if sys_name == 'win32' and username == 'gx':
    model = OllamaLLM(
        model="qwen2.5:14b",
        base_url='http://127.0.0.1:11434',
        temperature=0.1
    )
    print('user model {}'.format(model))
