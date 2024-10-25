import os

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

os.environ["HTTP_PROXY"] = ''
os.environ["HTTPS_PROXY"] = ''
os.environ["all_proxy"] = ''
os.environ["ALL_PROXY"] = ''

if __name__ == '__main__':

    template = """
你是一个给大家带来欢乐的喜剧演员。
    """

    # prompt_template = ChatPromptTemplate.from_messages([
    #     ('system', template),
    #     ('user', "{text}")
    # ])

    # 不使用模板
    messages = [
        SystemMessage(content=template),
        HumanMessage(content= "给我讲一个笑话"),
    ]

    model = OllamaLLM(model="qwen2.5:14b", base_url='http://125.69.16.175:11434')

    parser = StrOutputParser()

    # chain = prompt_template | model | parser

    # 不使用模板
    chain =  model | parser

    # stream_res = chain.stream({"text": "给我讲个笑话"})

    # 不使用模板
    stream_res = chain.stream(messages)
    content = ''
    for chunk in stream_res:
        # print(chunk)
        content += chunk
    print(content)
