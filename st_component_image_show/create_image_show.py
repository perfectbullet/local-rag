from typing import List, Dict

import streamlit.components.v1 as components


from jinja2 import Environment

def create_image_show(image_items: List[Dict], st):


    with open('./static/swiper-menu-gallery/index.html', 'rt', encoding='utf8') as f:
        html_content = f.read()
        # 创建模板引擎
        env = Environment()
        # 渲染模板
        template = env.from_string(html_content)
        result = template.render({'items': image_items})
        print('''****************************''')
        # st.html(result)
        # with st.container(border=True):
        components.html(result, width=1000, height=800)


if __name__ == '__main__':
    items = [
        {'url': 'http://127.0.0.1:8501/app/static/image_20241024/070148464112.jpg', 'imagename': 'imagename1'},
        {'url': 'http://127.0.0.1:8501/app/static/image_20241024/070327944112.jpg', 'imagename': 'imagename2'},
        {'url': 'http://127.0.0.1:8501/app/static/image_20241024/085621474266.jpg', 'imagename': 'imagename3'},
        {'url': 'http://127.0.0.1:8501/app/static/image_20241024/152254794100.jpg', 'imagename': 'imagename4'},
    ]
    create_image_show(items)