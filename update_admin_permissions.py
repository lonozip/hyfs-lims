import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'senaite_lims.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from core.models import Staff
from django.contrib.auth.models import User

try:
    # 获取用户 auf
    u = User.objects.get(username='auf')
    # 获取员工信息
    s = Staff.objects.get(user=u)
    
    # 授权所有权限
    s.can_manage_clients = True
    s.can_manage_orders = True
    s.can_manage_projects = True
    s.can_manage_samples = True
    s.can_manage_tests = True
    s.can_manage_reports = True
    s.can_manage_standard = True
    s.can_manage_staff = True
    s.can_manage_org = True
    s.can_manage_sample_types = True
    s.can_manage_sample_descriptions = True
    s.save()
    
    print('管理员 auf 的所有权限已授权完成')
    
except User.DoesNotExist:
    print('用户 auf 不存在')
except Staff.DoesNotExist:
    print('员工信息不存在')
except Exception as e:
    print(f'发生错误: {e}')
