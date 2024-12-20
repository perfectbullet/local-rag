import os

os.environ["HTTP_PROXY"] = ''
os.environ["HTTPS_PROXY"] = ''
os.environ["all_proxy"] = ''
os.environ["ALL_PROXY"] = ''
print('ok start of st medical llm chat')
from medical_components.chatbox import medical_llm_chatbox

from medical_components.page_config import set_page_config
from medical_components.page_state import set_initial_state

# 初始化页面
set_initial_state()

### Page Setup
set_page_config()
# set_page_header()

### Chat Box
medical_llm_chatbox()
