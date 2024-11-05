from langchain_community.llms import Ollama
llm = Ollama(model="llama3")


llm.invoke("how can langsmith help with testing?")
