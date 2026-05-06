import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'senaite_lims.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from core.models import Staff
from django.contrib.auth.models import User

try:
    # 获取用户
    u = User.objects.get(username='auf')
    # 获取员工信息
    s = Staff.objects.get(user=u)
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
except Staff.DoesNotExist:
    print('员工信息不存在')
except Exception as e:
    print(f'发生错误: {e}')
