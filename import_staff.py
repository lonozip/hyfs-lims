import os
import django
import sys

# 设置 Django 环境
sys.path.append('d:\\秦州_部门\\孟令飞_LIMS\\senaite.lims\\senaite_lims')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'senaite_lims.settings')
django.setup()

from core.models import Staff, Department
from django.contrib.auth.models import User

def import_staff():
    file_path = 'd:\\秦州_部门\\孟令飞_LIMS\\senaite.lims\\senaite_lims\\导入资料\\150位虚拟员工信息表（标准Markdown格式）.md'
    
    # 获取或创建一个默认用户作为创建者
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        admin_user = User.objects.create_user(username='temp_admin', password='password')

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    count = 0
    for line in lines:
        if line.startswith('|') and '人员名称' not in line and '---|---' not in line:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 7:
                name = parts[1]
                dept_name = parts[2]
                position = parts[3]
                email_raw = parts[4]
                phone = parts[5]
                address = parts[6]

                # 处理电子邮件中的 Markdown 链接格式 [email](mailto:email)
                import re
                email_match = re.search(r'\[(.*?)\]', email_raw)
                if email_match:
                    email = email_match.group(1).replace('\\', '')
                else:
                    email = email_raw

                # 获取或创建部门
                department, _ = Department.objects.get_or_create(
                    name=dept_name,
                    defaults={'created_by': admin_user}
                )

                # 创建员工
                # 检查是否已存在（根据姓名和电话简单判断）
                if not Staff.objects.filter(name=name, phone=phone).exists():
                    staff = Staff(
                        name=name,
                        department=department,
                        position=position if position != '未设置' else '',
                        email=email,
                        phone=phone,
                        address=address,
                        created_by=admin_user
                    )
                    staff.save()
                    count += 1
                    print(f'已导入: {name} ({dept_name})')

    print(f'总计导入 {count} 位员工。')

if __name__ == '__main__':
    import_staff()
