# 导入Django设置
import os
import sys

# 设置Django环境
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'senaite_lims.settings')

# 导入Django模块
import django
django.setup()

# 导入模型
from core.models import Client, Order

# 检查所有客户
print("所有客户:")
clients = Client.objects.all()
for client in clients:
    print(f"客户ID: {client.id}, 客户名称: {client.name}")
    # 检查该客户的订单
    orders = Order.objects.filter(client=client)
    print(f"  该客户的订单数量: {orders.count()}")
    for order in orders:
        print(f"  订单ID: {order.id}, 订单名称: {order.name}, 订单编号: {order.order_id}")

# 检查所有订单
print("\n所有订单:")
orders = Order.objects.all()
for order in orders:
    print(f"订单ID: {order.id}, 订单名称: {order.name}, 订单编号: {order.order_id}, 客户ID: {order.client.id}, 客户名称: {order.client.name}")
