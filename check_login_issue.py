import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'senaite_lims.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from core.models import Staff

# 检查用户 liusiyuan03@126.com
email = 'liusiyuan03@126.com'

print(f'检查用户: {email}')
print('=' * 50)

# 检查用户是否存在
try:
    user = User.objects.get(username=email)
    print(f'✓ 用户存在')
    print(f'  用户名: {user.username}')
    print(f'  邮箱: {user.email}')
    print(f'  激活状态: {user.is_active}')
    print(f'  超级用户: {user.is_superuser}')
    print(f'  员工状态: {user.is_staff}')
    
    # 尝试认证
    staff = Staff.objects.get(user=user)
    print(f'✓ 关联员工: {staff.name} ({staff.staff_id})')
    print(f'  员工启用状态: {staff.is_active}')
    
    # 尝试认证
    password = staff.staff_id or '123456'
    print(f'  尝试密码: {password}')
    authenticated = authenticate(username=email, password=password)
    if authenticated:
        print('✓ 认证成功！')
    else:
        print('✗ 认证失败！')
        
except User.DoesNotExist:
    print('✗ 用户不存在')
except Staff.DoesNotExist:
    print('✗ 没有关联的员工记录')
except Exception as e:
    print(f'✗ 发生错误: {e}')
