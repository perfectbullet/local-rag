GRAPH_EXTRACTION_PROMPT = """

-目标-

给定一个与此活动相关的文本文档和一组实体类型，从该文本中识别出所有属于这些类型的实体以及这些实体之间的所有关系。

-步骤-

1. 识别出所有实体。针对每个识别出的实体，提取以下信息:

- entity_name: 实体的名称，大写

- entity_type: 以下之一的实体类型:{entity_types}

将每个实体格式化为("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter})

2. 以英语的形式将步骤1中识别出的所有实体和关系返回为单个列表。使用**{record_delimiter}**作为列表分隔符。

4. 完成后，输出 {completion_delimiter}


######################

-示例-

######################

示例1:


实体类型:[医疗器械, 实验器材]

文本:

6.1  试验设备
试验设备包括:
a).    试验箱(室),并配有能保持和监控(见GJB     150.1A-2009 中的3.18)低气压条件所需要的辅助仪器；
b)     连续记录试验箱(室)内空气压力的装置。

################

输出:

("entity"{tuple_delimiter}"试验箱(室)"{tuple_delimiter}"实验器材"{tuple_delimiter}{record_delimiter})

("entity"{tuple_delimiter}"连续记录试验箱(室)内空气压力的装置"{tuple_delimiter}"实验器材"{tuple_delimiter}{record_delimiter})
#############################

示例2:


实体类型:[医疗器械, 实验器材]

文本:

6  试验要求
6.1  试验设备
6.1.1  总则
6.1.1.1  试验箱(室)密封性应良好。
6.1.1.2  使试件和试验装置接地，以避免静电荷的积累，并应按试件相应的安全要求检查电阻和(或) 电路连续性。
6.1.1.3  对于吹砂和吹尘试验箱，为了使扬起砂或尘的空气充分循环，要用一个足够大的试验箱，使 得试件占去的试验箱的横截面积(垂直于气流)不大于50%,占去的试验箱容积不大于30%。
6.1.1.4  使用与试验箱控制器分开的数据采集系统测量试验空间的条件(见 GJB     150.1A-2009  中 的 3.14),用可读出0.6℃以内读数的图表记录温度。
6.1.1.5  除了氮气之外，对试件周围的空气层进行除湿、加热和冷却所用的方法，不应改变试验箱试 验空间内的空气、尘、砂和水蒸气的化学成分。
6.1.2  吹尘
采用的试验设备包括试验箱和用以控制扬尘空气的尘浓度、风速、温度和湿度的辅助设备。用经校 准的烟尘计和标准光源一类的仪器保持和检查试验箱内循环尘的浓度。进入试验区去冲击试件的气流要 尽可能地接近于层流，至少要防止形成涡流。
6.1.3  吹砂
试验装置的设计应考虑：
a)    控制供砂器，使之以规定的浓度供砂。为了模拟现场产生的效果，供砂器的位置要能保证当冲 击试件时砂能近似均匀地悬浮在气流中。
注：当砂一空气的混合物垂直落下时，通常容易获得均匀的砂分布。
b)    由于吹砂的严重磨蚀特性，不要使砂循环流过风扇和调节控制空气温度的设备。
6.1.4  降尘
6.1.4.1  经验表明，为了使尘均匀地覆盖在试件的上面，试验区域的面积要足够大，最好采用水平面 积至少两倍于试件的面积的试验区域(见图1)。利用尘注入系统获得尘的均匀是困难的。采用的试验区 域的高度要足以保证能将试件周围的风速调节到接近于零(即小于0.2m/s)。为了满足此要求，经验表明， 使试验区域的高度4～5倍于试件的最大水平长度是必要的。
6.1.4.2  采用足以使尘扩散，并在试件上以0.25g/m²h(6g/m²/d±1g/m²/d)的速率产生均匀的尘沉降的 最小气流，将尘注入(持续不变或每小时一次)到试件上方(不直接注入到试件)的试验段，但要保证在试 件处的气流不超过0.2m/s。在试件的附近放置收集器来核查尘密度(勿靠近风扇入口)。在注入期间不要 打扰尘的沉降。要保证试件放置在水平面的中心，距任一箱壁或其他试件至少保持150mm(试件的抽风 风扇要求更远时除外)的距离。
6.1.4.3  由于难以控制尘的注入量，所以下面的尘注入系统已能良好地工作：在一个带有盖，盖上有 导管，导管上有细孔，通过细孔能吹压缩空气的玻璃筒中装上尘。空气流煽动起这些尘，这些尘通过一 个管导入尘注入系统。注入的尘的量取决于单位时间内压缩空气的体积、进入孔和尘的顶部之间的距离、 以及吹压缩空气的时间。由容器内的重量损耗粗略检测注入到试验箱内的尘的量。


#############

输出:

输出:

("entity"{tuple_delimiter}"试验箱(室)"{tuple_delimiter}"实验器材"{tuple_delimiter}{record_delimiter})

("entity"{tuple_delimiter}"烟尘计"{tuple_delimiter}"实验器材"{tuple_delimiter}{record_delimiter})

("entity"{tuple_delimiter}"标准光源"{tuple_delimiter}"实验器材"{tuple_delimiter}{record_delimiter})

("entity"{tuple_delimiter}"供砂器"{tuple_delimiter}"实验器材"{tuple_delimiter}{record_delimiter})

#############################

示例3:



实体类型:[医疗器械, 实验器材]

文本:

三申卧式圆形压力蒸汽灭菌器

三申卧式圆形压力蒸汽灭菌器性能特点

　　1.产品容器的器身选用不锈钢材质制成，经久耐用。

　　2.三申卧式圆形压力蒸汽灭菌器微电脑全过程自动控制。

　　3.LED数码全面显示设置和动态的温度、计时值。

　　4.水箱和灭菌室采用双压力、双温度显示和控制。

　　5.LED灯和报警装置全方位指示设备运行状态。

　　6.PID控温功能，通过选择可以自动修正加热控制参数，防止冲温。

　　7.控温精度±0.5℃。

　　8.超温(设定温度+2℃)报警，停止加热。

　　9.具有自动补水功能，缺水停止加热、补水、到达低水位后继续加热，按顺序进行。

　　10.安全阀超压保护。

　　11.灭菌器门有电子联锁装置，保证门没有到位、锁没有锁住手轮不供汽工作。灭菌室在有压条件下门锁不能打开，手轮不能旋转，门不能开启。

　　12.自胀式硅橡胶密封圈密封效果好，使用寿命长。

　　13.在保持水箱连续运行的状态下，具备烘干功能。

　　14.保温结束后的排汽方式可选择，适应不同类型的物质灭菌后的泄压要求。


#############

输出:

("entity"{tuple_delimiter}"三申卧式圆形压力蒸汽灭菌器"{tuple_delimiter}"医疗器械"{tuple_delimiter}{record_delimiter})


"""


import os

from langchain_core.messages import SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

os.environ["HTTP_PROXY"] = ''
os.environ["HTTPS_PROXY"] = ''
os.environ["all_proxy"] = ''
os.environ["ALL_PROXY"] = ''

if __name__ == '__main__':
    user_prompt = '''
#############################

-真实数据-

######################

实体类型:{entity_types}
文本:{input_text}
######################'''

    demo_input = '''6.1  试验设备
6.1.1     程序I
6.1.1.1  使用能以本部分规定的速率产生降雨的淋雨设备。当雨水分配器产生降雨时，该装置产生雨 滴直径范围在0.5mm～4.5mm 之间。当伴有规定风速的风时，应确保该降雨喷散到整个试件上，可在 雨水中加入荧光素一类的水溶性染料，以帮助定位和分析水渗漏。对稳态雨既可采用喷嘴也可采用图1 所示的装置(去掉聚乙烯管),水分配器位置要足够高，采用的滴水高度应确保水滴的最终速度均 为 9m/s。
6.1.1.2  根据试件来布置风源位置，以使雨水具有水平方向到45°的变化，并均匀地扑打在试件一侧 面。水平风速应不小于18m/s,  在试件放入试验装置前于试件处测量。
6.1.2     程序II
所有喷嘴应产生水压约为276kPa、雨滴尺寸在0.5mm～4.5mm  范围内的方格喷淋网阵或其他形式 的交错水网阵，以达到最大的表面覆盖。在每0.56m² 接受淋雨的表面范围内，且在距试件表面48mm   处至少有一个喷嘴。必要时可调整此距离以达到喷淋网的交叠。雨水中可加入荧光素一类的水溶性染料， 以帮助定位和分析任何水渗漏，按图2定位喷嘴。
6.1.3     程序ⅢI

GJB            150.8A-2009


使用的试验装置应能提供大于280L/m²h  的滴水量，水从分配器中滴出，但不能聚成水流。分配器 上有以20mm～25.4mm 间隔点阵分布的滴水孔。分配器按图1和图3所示进行结构设计，推荐用图1, 主要是由于它的构造和维护简单，成本较低且试验重现性好。聚乙烯套管可任选，采用的滴水高度应确 保水滴的最终速度约为9m/s。同时采用的水分配器应有足够大的面，以覆盖试件的整个上表面。雨水 中可加入荧光素一类的水溶性燃料，以帮助定位和分析水渗漏。'''

    prompt_template = ChatPromptTemplate.from_messages([
        ('system', GRAPH_EXTRACTION_PROMPT),
        ('user', user_prompt)
    ])

    # tuple_delimiter: The delimiter for tuples. Default is "<|>".
    #
    # record_delimiter: The delimiter for records. Default is "##".
    #
    # completion_delimiter: The delimiter for completions. Default is "<|COMPLETE|>".

    t = prompt_template.invoke({
        "entity_types": "[医疗器械, 实验器材]",
        "input_text": demo_input,
        'tuple_delimiter': '<|>',
        'record_delimiter': '##',
        'completion_delimiter': '<|COMPLETE|>',
    })
    model = OllamaLLM(model="qwen2.5:14b", base_url='http://125.69.16.175:11434')

    parser = StrOutputParser()

    chain = prompt_template | model | parser

    stream_res = chain.invoke({""
                               "entity_types": "[医疗器械, 实验器材]",
                               "input_text": demo_input,
                               'tuple_delimiter': '<|>',
                               'record_delimiter': '##',
                               'completion_delimiter': '<|COMPLETE|>',
                               })
    print(stream_res)