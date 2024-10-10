import os

# os.environ["HTTP_PROXY"] = 'http://127.0.0.1:58591'
# os.environ["HTTPS_PROXY"] = 'http://127.0.0.1:58591'
# os.environ["all_proxy"] = ''
# os.environ["ALL_PROXY"] = ''
print('ok start of st')
from components.chatbox import chatbox
# from components.header import set_page_header

from components.page_config import set_page_config
from components.page_state import set_initial_state

## Setup Initial State
set_initial_state()

### Page Setup
set_page_config()
# set_page_header()

### Sidebar
# sidebar()

### Chat Box
chatbox()
