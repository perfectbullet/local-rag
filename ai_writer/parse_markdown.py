import re
from collections import defaultdict


def parse_markdown(md_filepath):
    markdown_text = ''
    with open(md_filepath, 'r', encoding='utf8') as f:
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
    # logger.info('structured_data is {}', structured_data)
    return structured_data