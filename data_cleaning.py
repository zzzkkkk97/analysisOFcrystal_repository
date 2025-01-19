import pandas as pd
import re


def isLegal(text):
    # 检查非 ASCII 字符比例
    non_ascii_count = sum(1 for char in text if ord(char) >= 128)
    non_ascii_ratio = non_ascii_count / len(text) if text else 0
    if non_ascii_ratio > 0.5:  # 非 ASCII 字符比例超过 50% 认为可能是乱码
        return True

    # 检查无效的 Unicode 字符组合
    # 这里简单检查是否有连续的代理对（无效的 Unicode 组合）
    if re.search(r'[\ud800-\udbff][\udc00-\udfff]{2,}', text):
        return True

    # 检查是否有孤立的控制字符
    if re.search(r'[\x00-\x1f](?![\x00-\x1f])', text):
        return True

    return False


def data_cleaning(input_file_path, output_file_path):
    # 加载数据
    data = pd.read_csv(input_file_path)

    # 去除重复行
    data = data.drop_duplicates()

    # 检查并处理乱码（更新内容描述和 Update Type）
    for col in ['Update Content', 'Update Type']:
        data = data[~data[col].apply(isLegal)]

    # 检查 View Count 的值是否大于 0
    data = data[data['View Count'] > 0]

    # 检查和修正 Update Time 列的数据格式为日期格式
    try:
        data['Update Time'] = pd.to_datetime(data['Update Time'])
    except ValueError as e:
        print(f"日期转换错误: {e}")

    # 保存清洗后的数据
    data.to_csv(output_file_path, index=False)

# 输入和输出文件路径
input_file_path = 'C:/Users/86137/Desktop/issues_data.csv'
output_file_path = 'C:/Users/86137/Desktop/issues_data_cleaned.csv'

# 调用函数进行数据清洗
data_cleaning(input_file_path, output_file_path)

