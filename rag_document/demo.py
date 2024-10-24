import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

os.environ["HTTP_PROXY"] = ''
os.environ["HTTPS_PROXY"] = ''
os.environ["all_proxy"] = ''
os.environ["ALL_PROXY"] = ''

template = """Question: {question}
Answer: Let's think step by step."""

prompt = ChatPromptTemplate.from_template(template)

model = OllamaLLM(model="llama3", base_url='http://125.69.16.175:11434/v1')

chain = prompt | model

res = chain.invoke({"question": "What is LangChain?"})
print(res)


