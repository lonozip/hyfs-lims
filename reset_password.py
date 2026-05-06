import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'senaite_lims.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth.models import User

# 重置刘思远的密码为 12345
email = 'liusiyuan03@126.com'

try:
    user = User.objects.get(username=email)
    user.set_password('12345')
    user.save()
    print(f'已将 {email} 的密码重置为 12345')
except User.DoesNotExist:
    print('用户不存在')
except Exception as e:
    print(f'发生错误: {e}')
