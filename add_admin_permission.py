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
    
    # 添加管理后台权限
    s.can_access_admin = True
    s.save()
    
    print('管理员 auf 已添加管理后台权限')
    
except User.DoesNotExist:
    print('用户 auf 不存在')
except Staff.DoesNotExist:
    print('员工信息不存在')
except Exception as e:
    print(f'发生错误: {e}')
