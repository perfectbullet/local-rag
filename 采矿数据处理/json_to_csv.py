# 依赖：pip install pandas openpyxl
import json
import os

import pandas as pd
import argparse

def save_json(data, file_path):
    # 读取JSON文件
    with open(file_path, 'w', encoding='utf-8') as f:
        data = json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"操作成功！文件路径：{file_path}")


def read_json(json_dir):
    '''
    Args:
        json_dir:
    Returns:
    '''
    total_data = []
    for root, dirs, files in os.walk(json_dir):
        for file in files:
            if file.endswith('.json'):
                input_file = os.path.join(root, file)
                # 读取JSON文件
                with open(input_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for d in data:
                        d['title'] = file.replace('.json', '')
                    total_data.extend(data)
    return total_data


def json_to_excel(data, output_file):
    """
    Args:
        data:
        output_file:
    Returns:
    """
    try:
        df_new = pd.DataFrame(data)
        # # 判断文件是否存在
        # if os.path.exists(output_file):
        #     # 读取现有Excel内容
        #     df_old = pd.read_excel(output_file, engine='openpyxl')
        #
        #     # 垂直合并新旧数据
        #     df_combined = pd.concat([df_old, df_new], ignore_index=False)
        # else:
        #     df_combined = df_new

        # 生成/更新Excel文件
        df_new.to_excel(output_file, index=True, engine='openpyxl')
        print(f"操作成功！文件路径：{output_file}")

    except PermissionError:
        print("错误：Excel文件正在被其他程序使用，请关闭后重试")
    except Exception as e:
        print(f"操作失败：{str(e)}")


def json_dir2excel(json_dir, output_file, output_json):
    """

    Args:
        json_dir:
        output_file:
        output_json:

    Returns:

    """
    total_data = read_json(json_dir)
    print(f'一共有{len(total_data)}条数据')
    save_json(total_data, output_json)
    json_to_excel(total_data, output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir', default='json格式问答对', help='输入JSON目录')
    parser.add_argument('-o', '--output', default='output.xlsx', help='输出Excel文件')
    parser.add_argument('-oj', '--output_json', default='output.json', help='输出json文件')
    args = parser.parse_args()
    json_dir2excel(args.dir, args.output, args.output_json)
