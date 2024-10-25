import os

from langchain_core.messages import SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

os.environ["HTTP_PROXY"] = ''
os.environ["HTTPS_PROXY"] = ''
os.environ["all_proxy"] = ''
os.environ["ALL_PROXY"] = ''

if __name__ == '__main__':

    template = """"""

    prompt_template = ChatPromptTemplate.from_messages([
        ('system', template),
        # ('user', '{text}')
    ])

    model = OllamaLLM(model="qwen2.5:14b", base_url='http://125.69.16.175:11434')

    parser = StrOutputParser()

    chain = prompt_template | model | parser

    stream_res = chain.stream({"question": "What is LangChain?"})
    for chunk in stream_res:
        print(chunk)
