import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'senaite_lims.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from core.models import Staff

try:
    # 获取所有有关联用户的员工
    staff_with_user = Staff.objects.filter(user__isnull=False)
    count = 0
    
    for staff in staff_with_user:
        # 设置密码为12345
        staff.user.set_password('12345')
        staff.user.save()
        count += 1
        print(f'已更新: {staff.name} ({staff.staff_id}) - {staff.user.username}')
    
    print(f'\n共更新 {count} 个员工账号的密码')
    
except Exception as e:
    print(f'发生错误: {e}')
