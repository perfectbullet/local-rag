# import time
# import mammoth
# import markdownify
# # 转存Word文档内的图片
# def convert_imgs(image):
#     with image.open() as image_bytes:
#         file_suffix = image.content_type.split("/")[1]
#         path_file = "./img/{}.{}".format(str(time.time()),file_suffix)
#         with open(path_file, 'wb') as f:
#             f.write(image_bytes.read())

#     return {"src":path_file}

# # 读取Word文件
# with open(r"/data/wsx_workspace/gx_demos/ai_writer/template.docx", "rb") as docx_file:
#     # 转化Word文档为HTML
#     result = mammoth.convert_to_html(docx_file,convert_image = mammoth.images.img_element(convert_imgs))
#     # 获取HTML内容
#     html = result.value
#     # 转化HTML为Markdown
#     md = markdownify.markdownify(html,heading_style="ATX")
#     print(md)
#     with open("./docx_to_html.html",'w',encoding='utf-8') as html_file,open("./docx_to_md.md","w",encoding='utf-8') as md_file:
#         html_file.write(html)
#         md_file.write(md)
#     messages = result.messages

import re
from collections import defaultdict

def parse_markdown(md_filepath):
    markdown_text = ''
    with open(md_filepath,'r') as f:
        for l in f.readlines():
            markdown_text += l
    # 结构化数据存储
    structured_data = defaultdict(lambda: defaultdict(str))
    
    # 正则表达式匹配标题
    h1_pattern = re.compile(r'^## (.+)', re.MULTILINE)
    h2_pattern = re.compile(r'^### (.+)', re.MULTILINE)
    
    # 查找所有一级标题
    h1_matches = list(h1_pattern.finditer(markdown_text))
    
    for i, h1_match in enumerate(h1_matches):
        h1_title = h1_match.group(1).strip()
        h1_start = h1_match.end()
        h1_end = h1_matches[i + 1].start() if i + 1 < len(h1_matches) else len(markdown_text)
        
        # 获取一级标题下的内容
        h1_content = markdown_text[h1_start:h1_end]
        
        # 查找所有二级标题
        h2_matches = list(h2_pattern.finditer(h1_content))
        
        if not h2_matches:
            # 如果没有二级标题，直接存储一级标题的内容
            structured_data[h1_title] = h1_content.strip()
        else:
            for j, h2_match in enumerate(h2_matches):
                h2_title = h2_match.group(1).strip()
                h2_start = h2_match.end()
                h2_end = h2_matches[j + 1].start() if j + 1 < len(h2_matches) else len(h1_content)
                
                # 获取二级标题下的内容
                h2_content = h1_content[h2_start:h2_end].strip()
                
                # 去除二级标题本身的行
                h2_content = re.sub(r'^## .+', '', h2_content, flags=re.MULTILINE).strip()
                
                # 存储二级标题及其内容
                structured_data[h1_title][h2_title] = h2_content
    
    return structured_data

# 解析Markdown文本
structured_data = parse_markdown('/data/wsx_workspace/gx_demos/ai_writer/docx_to_md.md')

for h1, h2_data in structured_data.items():
    if isinstance(h2_data, str):
        print(f"一级标题: {h1}")
        print(f"  内容: {h2_data}")
    else:
        print(f"一级标题: {h1}")
        for h2, content in h2_data.items():
            print(f"  二级标题: {h2}")
            print(f"    内容: {content}")
