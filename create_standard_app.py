import os
import django

# 设置Django设置模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'senaite_lims.settings')

# 初始化Django
django.setup()

# 运行创建应用的命令
from django.core.management import call_command
print("创建 standard 应用...")
call_command('startapp', 'standard')
print("应用创建完成！")