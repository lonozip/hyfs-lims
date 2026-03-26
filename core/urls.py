# 导入Django路径函数
from django.urls import path
# 导入当前应用的视图模块
from . import views

# URL模式列表
urlpatterns = [
    # 首页URL
    path('', views.home, name='home'),
    # 注册URL
    path('register/', views.register, name='register'),
    # 客户列表URL
    path('clients/', views.client_list, name='client_list'),
    # 客户删除URL
    path('clients/<int:pk>/delete/', views.client_delete, name='client_delete'),
    # 样品列表URL
    path('samples/', views.sample_list, name='sample_list'),
    # 样品删除URL
    path('samples/<int:pk>/delete/', views.sample_delete, name='sample_delete'),
    # 测试列表URL
    path('tests/', views.test_list, name='test_list'),
    # 订单列表URL
    path('orders/', views.order_list, name='order_list'),
    # 订单删除URL
    path('orders/<int:pk>/delete/', views.order_delete, name='order_delete'),
    # 员工列表URL
    path('staff/', views.staff_list, name='staff_list'),
    # 项目方案列表URL
    path('project_orders/', views.project_order_list, name='project_order_list'),
    # 项目方案详情URL
    path('project_orders/<int:pk>/', views.project_order_detail, name='project_order_detail'),
    # 项目方案删除URL
    path('project_orders/<int:pk>/delete/', views.project_order_delete, name='project_order_delete'),
    # 报告列表URL
    path('reports/', views.report_list, name='report_list'),
    # 报告详情URL
    path('reports/<int:pk>/', views.report_detail, name='report_detail'),
    # 报告审核URL
    path('reports/<int:pk>/approve/', views.report_approve, name='report_approve'),
    # 报告生成PDF URL
    path('reports/<int:pk>/generate_pdf/', views.generate_pdf_report, name='generate_pdf_report'),
    # 报告删除URL
    path('reports/<int:pk>/delete/', views.report_delete, name='report_delete'),
    # 标准管理URL
    path('standard/', views.standard_list, name='standard_list'),
    # 获取订单的AJAX URL
    path('sample/get_orders/', views.get_orders, name='get_orders'),
    
]