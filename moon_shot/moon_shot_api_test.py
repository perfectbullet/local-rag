import os

from openai import OpenAI

os.environ["HTTP_PROXY"] = ''
os.environ["HTTPS_PROXY"] = ''
os.environ["all_proxy"] = ''
os.environ["ALL_PROXY"] = ''

# OPENAI_API_KEY  月之暗面 2024-12-10
# sk-BhazmM2Qz12BXRYejKXMhibmTn2uuBrhOQv6bwcJgNVYBiBB

# export https_proxy=http://127.0.0.1:7897 http_proxy=http://127.0.0.1:7897 all_proxy=socks5://127.0.0.1:7897

client = OpenAI(
    api_key="sk-BhazmM2Qz12BXRYejKXMhibmTn2uuBrhOQv6bwcJgNVYBiBB",
    base_url="https://api.moonshot.cn/v1",
)
