import os
from moon_shot.moon_shot_api_test import client

sys_prompt = "现在你是一个军事领域的英汉翻译器，当我输入中文时，你翻译成英文。当我连续输入多个英文词时，默认按照句子翻译成中文。翻译句子和段落时，要注意联系上下文，注意武器专有名称不用翻译。你的翻译成果应该接近于一个母语者。你以军事解说的语言风格来翻译。"

for root, dirs,  files in os.walk('D:\zj_work\兵棋推演DB\Descriptions'):
    for name in files:
        with open(os.path.join(root, name), 'rt') as f:
            content = f.read()
            completion = client.chat.completions.create(
                model="moonshot-v1-8k",
                messages=[
                    {"role": "system",
                     "content": sys_prompt},
                    {"role": "user", "content": content}
                ],
                temperature=0.3,
            )

            translation_content = completion.choices[0].message.content
            print(translation_content)
