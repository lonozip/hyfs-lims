import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'senaite_lims.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from core.models import Staff
from django.contrib.auth.models import User

print('所有用户:')
for u in User.objects.all():
    print(f'  - {u.username} ({u.email})')

print('\n所有员工:')
for s in Staff.objects.all():
    print(f'  - {s.name} ({s.staff_id})')
    if s.user:
        print(f'    用户: {s.user.username}')
