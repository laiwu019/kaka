#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import json

# 读取Excel
file_path = r'H:\outputs\customer-referrals-20261020\客户专属注册链接_每人12条_20261020.xlsx'
df = pd.read_excel(file_path)

# 提取数据为数组格式
customers = []
for _, row in df.iterrows():
    name = str(row['客户名称']).strip()
    if name == 'nan' or not name:
        continue

    customer = {'name': name}
    for i in range(1, 13):  # 链接1 到 链接12
        link = str(row[f'链接{i}']).strip()
        if link and link != 'nan':
            customer[f'link{i}'] = link

    if len(customer) > 1:  # 至少有name和一条链接
        customers.append(customer)

print(f'提取了 {len(customers)} 个客户')
print(f'第一个客户: {customers[0]["name"]}, 有 {len([k for k in customers[0].keys() if k.startswith("link")])} 条链接')

# 读取HTML模板
with open('customer-links.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 找到数据插入位置
import re
pattern = r'const PRELOADED_DATA = \[.*?\];'
json_data = json.dumps(customers, ensure_ascii=False, indent=2)
replacement = f'const PRELOADED_DATA = {json_data};'
html_new = re.sub(pattern, replacement, html, flags=re.DOTALL)

if html_new == html:
    print('警告：没有找到PRELOADED_DATA，尝试查找其他模式')
    # 如果没找到，尝试直接在script标签后插入
    pattern2 = r'(<script>\s*(?://[^\n]*\n)?)'
    replacement2 = f'\\1        const PRELOADED_DATA = {json_data};\n'
    html_new = re.sub(pattern2, replacement2, html, count=1)

# 保存
with open('customer-links.html', 'w', encoding='utf-8') as f:
    f.write(html_new)

print('已更新 customer-links.html')

# 验证
if 'link12' in html_new:
    print('✓ 确认包含12条链接')
else:
    print('⚠ 未找到link12字段')
