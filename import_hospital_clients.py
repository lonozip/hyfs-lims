#!/usr/bin/env python
"""导入陕西及周边地区医院虚拟客户数据脚本"""
import os
import sys
import re

sys.path.insert(0, r'd:\秦州_部门\孟令飞_LIMS\senaite.lims\senaite_lims')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "senaite_lims.settings")

import django
django.setup()

from core.models import Client
from django.contrib.auth.models import User

# 从markdown文件中解析客户数据
md_file_path = r'd:\秦州_部门\孟令飞_LIMS\senaite.lims\senaite_lims\导入资料\陕西及周边地区医院虚拟客户名单.md'

# 读取文件内容
with open(md_file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 打印文件内容用于调试
print("文件内容片段:")
lines = content.split('\n')
for i, line in enumerate(lines[:10]):
    print(f"{i}: {repr(line)}")

# 使用正则表达式匹配表格数据行
# 格式: |西安市第一人民医院|陕西省西安市碑林区|王建国|13991801001|wangjianguo@xadyyy.com|三级甲等|
pattern = r'\|([^|]+)\|([^|]+)\|([^|]+)\|([^|]+)\|([^|]+)\|([^|]+)\|'
matches = re.findall(pattern, content)

clients_data = []
for match in matches:
    name, region, contact, phone, email, hospital_level = match
    
    # 从邮箱中提取纯邮箱地址（移除mailto链接）
    email = re.sub(r'<mailto:([^>]+)>', r'\1', email)
    email = email.replace('\\.', '.').strip()
    
    # 从所属地区提取省份、城市、地址
    # 格式: 陕西省西安市碑林区 -> 省份:陕西省, 城市:西安市, 地址:碑林区
    region = region.strip()
    province = ''
    city = ''
    address = ''
    
    # 尝试解析地区信息
    region_pattern = r'([省自治区]+)?([^省]+市)?(.+)?'
    region_match = re.match(r'(.+省)(.+市)(.+)', region)
    if region_match:
        province = region_match.group(1)
        city = region_match.group(2)
        address = region_match.group(3)
    else:
        # 如果解析失败，将整个地区作为地址
        address = region
    
    clients_data.append({
        'name': name.strip(),
        'contact_person': contact.strip(),
        'email': email,
        'phone': phone.strip(),
        'province': province.strip(),
        'city': city.strip(),
        'address': address.strip()
    })

print(f"\n共解析到 {len(clients_data)} 条客户数据")
for i, c in enumerate(clients_data[:3]):
    print(f"{i+1}. {c['name']} - {c['contact_person']} - {c['email']}")

# 获取默认用户作为创建人
default_user = User.objects.filter(is_superuser=True).first()
if not default_user:
    default_user = User.objects.first()
    if not default_user:
        print("未找到用户，请先创建用户")
        sys.exit(1)

# 导入数据
imported_count = 0
skipped_count = 0
for data in clients_data:
    # 检查是否已存在
    if Client.objects.filter(name=data['name']).exists():
        print(f"跳过已存在客户: {data['name']}")
        skipped_count += 1
        continue

    # 创建客户
    client = Client.objects.create(
        name=data['name'],
        contact_person=data['contact_person'],
        email=data['email'],
        phone=data['phone'],
        province=data['province'],
        city=data['city'],
        address=data['address'],
        created_by=default_user
    )
    print(f"成功导入客户: {data['name']}")
    imported_count += 1

print(f"\n导入完成！新增: {imported_count} 条, 跳过(已存在): {skipped_count} 条")