from openai import OpenAI
import os


def get_response():
    # client = OpenAI(
    #     api_key="sk-60f7dab83508414f94ec5c9c86751c53", # 如果您没有配置环境变量，请在此处用您的API Key进行替换
    #     base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")
    client = OpenAI(
    api_key='None',base_url="http://localhost:18400/v1"
)
    selected_text = """在我们所处的数字化时代，业务场景的复杂性与日俱增，由此产生的文档管理需求呈现出爆炸式的增长。传统办公模式，受限于其固有的局限性，逐渐暴露出效能瓶颈，尤其是在处理文档任务时，其效率低下问题日益显著，同时对软件需求规格的准确性与处理速度提出了前所未有的高要求。为适应这一发展态势，行业对于专业人才的技能要求也随之提高，单纯依赖人力操作已难以满足快速变化的业务环境需求。
"""
    system = """ ## 角色描述：你是一名项目写作专家，擅长对项目申请书中的文字进行润色。
    ## 工作流程
    第一步：在开始润色之前，必须认真阅读并牢记润色的要求。
    第二步：使用Markdown格式，按照润色的要求，对给你的文字进行润色。
        """
    user = f"""
    原文字如下:
    {selected_text}
    润色要求如下:
    重点突出AI的好处
        """
    completion = client.chat.completions.create(
        model="qwen7b",
        messages=[{'role': 'system', 'content': system},
                  {'role': 'user', 'content': user}],
        stream=True,
        n=3,
        # temperature=1.5,
        # top_p=0.9,
        # max_tokens=1000,
        )
    # 用于存储每个响应的当前部分
    current_response = ""
    current_index = 0
    stream1 = ""
    stream2 = ""
    stream3 = ""
    for idx, message in enumerate(completion):
        if message.choices[0].finish_reason is not None:  # 检查是否完成
            continue
        if message.choices[0].delta.content is not None:
            if idx % 3 == 0:
                stream1 += message.choices[0].delta.content
            elif idx % 3 == 1:
                stream2 += message.choices[0].delta.content
            elif idx % 3 == 2:
                stream3 += message.choices[0].delta.content
    # 分别打印三个流式输出的内容
    print("Stream 1 Output:\n", stream1)
    print("Stream 2 Output:\n", stream2)
    print("Stream 3 Output:\n", stream3)
    # full_response = ['','','']
    # index=0
    # for chunk in completion:
    #     chunk = chunk.choices
    #     if chunk and chunk[0].delta.content is not None:
    #         full_response[index%3] += chunk[0].delta.content
    #     index+=1

    # print(full_response)
    
if __name__ == '__main__':
    get_response()