import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'senaite_lims.settings')
import django
django.setup()

from core.models import Sample

# 获取所有样本
samples = Sample.objects.all()
print(f'总样本数: {samples.count()}')
print('\n样本ID列表:')
for sample in samples[:10]:
    project_id = sample.project_order.project_id if sample.project_order else '无'
    print(f'  {sample.sample_id} - 方案: {project_id}')
