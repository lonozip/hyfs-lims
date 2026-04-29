#!/usr/bin/env python
"""导入虚拟客户数据脚本"""
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
md_file_path = r'd:\秦州_部门\孟令飞_LIMS\senaite.lims\senaite_lims\导入资料\虚拟客户资料（30条）.md'

# 读取文件内容
with open(md_file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 打印文件内容用于调试
print("文件内容片段:")
lines = content.split('\n')
for i, line in enumerate(lines[:20]):
    print(f"{i}: {repr(line)}")

# 使用正则表达式匹配表格数据行
# 格式: |1|恒信致远科技有限公司|张磊|zhanglei@hxzytech\.com|13800138001|北京市|北京市|朝阳区建国路88号现代城A座1502室|
pattern = r'\|(\d+)\|([^|]+)\|([^|]+)\|([^|]+)\|(\d+)\|([^|]+)\|([^|]+)\|([^|]+)\|'
matches = re.findall(pattern, content)

clients_data = []
for match in matches:
    seq, name, contact, email, phone, province, city, address = match
    # 清理HTML标签
    address = re.sub(r'<[^>]+>', '', address).strip()
    clients_data.append({
        'name': name.strip(),
        'contact_person': contact.strip(),
        'email': email.strip(),
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