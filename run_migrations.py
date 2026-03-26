import os
import django

# 设置Django设置模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'senaite_lims.settings')

# 初始化Django
django.setup()

# 运行迁移命令
from django.core.management import call_command
print("运行 makemigrations...")
call_command('makemigrations')
print("运行 migrate...")
call_command('migrate')
print("迁移完成！")