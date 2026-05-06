import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'senaite_lims.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from core.models import Staff, Department, Position
from django.contrib.auth.models import User

try:
    # 获取用户
    u = User.objects.get(username='auf')
    
    # 检查是否已有员工关联
    try:
        s = Staff.objects.get(user=u)
        print(f'员工已存在: {s.name}')
    except Staff.DoesNotExist:
        # 获取第一个部门作为默认部门
        dept = Department.objects.first()
        if not dept:
            dept = Department.objects.create(name='默认部门')
        
        # 创建员工记录
        s = Staff.objects.create(
            name='管理员',
            staff_id='STAFF-ADMIN-001',
            user=u,
            email=u.email,
            department=dept,
            is_active=True
        )
        print(f'已创建员工: {s.name}')
    
    # 授权所有权限
    s.can_manage_clients = True
    s.can_manage_orders = True
    s.can_manage_samples = True
    s.can_manage_tests = True
    s.can_manage_reports = True
    s.can_manage_staff = True
    s.save()
    print('权限已全部授权')
    
except User.DoesNotExist:
    print('用户 auf 不存在')
except Exception as e:
    print(f'发生错误: {e}')
