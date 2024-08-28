"""
* -*- coding: utf-8 -*-
* @Time : 2024/8/8 16:00
* @Author : liwei
* @File : sum_amount.py
"""

import os
from paddleocr import PaddleOCR
import pandas as pd

# 初始化PaddleOCR识别器，设置语言为中文，并启用方向分类器
ocr = PaddleOCR(use_angle_cls=True, lang='ch')

# 设置PDF文件夹路径
pdf_folder = r'C:\Users\THINK\Desktop\发票'

# 初始化总金额
total_amount = 0

# excel表格数据
invoice_data = []


# 辅助函数：提取金额信息
def extract_amount(text):
    import re
    # 正则表达式匹配金额，例如匹配￥后跟数字和小数点
    match = re.search(r'[￥¥]([\d.]+)', text)
    if match:
        return float(match.group(1))
    return 0.0


# 遍历文件夹中的所有PDF文件
index = 1
for pdf_filename in os.listdir(pdf_folder):
    if pdf_filename.endswith('.pdf'):
        pdf_path = os.path.join(pdf_folder, pdf_filename)

        # 使用PaddleOCR识别PDF中的文本
        result = ocr.ocr(pdf_path, cls=True)

        # 假设result是一个列表，其中每个元素是一页的识别结果
        invoice_json = {
            "序号": 0,
            "发票提供者": "",
            "发票内容": "",
            "开票日期": "",
            "金额": "",
            "发票号码": "",
            "是否电子发票": "",
        }
        for page_result in result:
            invoice_json["序号"] = index
            for line in page_result:
                # 提取金额，这里需要根据实际文本格式编写正则表达式
                if '名称：' in line[1][0]:
                    name = line[1][0].split('：')[1]
                    if name != '中国电信股份有限公司上海分公司':
                        invoice_json['发票提供者'] = name
                        print(name)
                invoice_json['发票内容'] = '餐饮'
                if '开票日期' in line[1][0]:
                    invoice_date = line[1][0].split('：')[1]
                    invoice_json['开票日期'] = invoice_date
                if '小写' in line[1][0]:
                    print(line[1][0])
                    amount = extract_amount(line[1][0])
                    invoice_json['金额'] = amount
                    total_amount += amount
                if '发票号码' in line[1][0]:
                    invoice_number = line[1][0].split('：')[1]
                    invoice_json['发票号码'] = invoice_number
                invoice_json['是否电子发票'] = '是'

        index += 1
        invoice_data.append(invoice_json)

print(invoice_data)

# 创建DataFrame
df = pd.DataFrame(invoice_data)

# 将DataFrame写入Excel文件
excel_filename = 'invoices.xlsx'
df.to_excel(excel_filename, index=False, engine='openpyxl')

total_amount = total_amount
# 打印总金额
print(f'总金额为: {total_amount}')

