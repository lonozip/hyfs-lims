# 导入Django路径函数
from django.urls import path
# 导入当前应用的视图模块
from . import views

# 简单的测试视图
from django.http import HttpResponse
def test_view(request):
    return HttpResponse('Hello, World!')

# URL模式列表
urlpatterns = [
    # 测试视图URL
    path('test/', test_view, name='test_view'),
    # 首页URL
    path('', views.home, name='home'),
    # 注册URL
    path('register/', views.register, name='register'),
    # 客户列表URL
    path('clients/', views.client_list, name='client_list'),
    # 客户添加URL
    path('clients/create/', views.client_create, name='client_create'),
    # 客户编辑URL
    path('clients/<int:pk>/edit/', views.client_edit, name='client_edit'),
    # 客户删除URL
    path('clients/<int:pk>/delete/', views.client_delete, name='client_delete'),
    # 样品列表URL
    path('samples/', views.sample_list, name='sample_list'),
    # 按方案显示样品列表URL
    path('samples/project/<str:project_id>/', views.sample_list, name='sample_list_by_project'),
    # 样品添加URL
    path('samples/create/', views.sample_create, name='sample_create'),
    # 样品编辑URL
    path('samples/<int:pk>/edit/', views.sample_edit, name='sample_edit'),
    # 样品删除URL
    path('samples/<int:pk>/delete/', views.sample_delete, name='sample_delete'),
    # 测试列表URL
    path('tests/', views.test_list, name='test_list'),
    # 按方案显示测试列表URL
    path('tests/project/<str:project_id>/', views.test_list, name='test_list_by_project'),
    # 测试添加URL
    path('tests/create/', views.test_create, name='test_create'),
    # 测试编辑URL
    path('tests/<int:pk>/edit/', views.test_edit, name='test_edit'),
    # 订单列表URL
    path('orders/', views.order_list, name='order_list'),
    # 订单添加URL
    path('orders/create/', views.order_create, name='order_create'),
    # 订单编辑URL
    path('orders/<int:pk>/edit/', views.order_edit, name='order_edit'),
    # 订单删除URL
    path('orders/<int:pk>/delete/', views.order_delete, name='order_delete'),
    # 员工列表URL
    path('staff/', views.staff_list, name='staff_list'),
    # 组织架构管理URL
    path('org/', views.org_manage, name='org_manage'),
    path('department/create/', views.department_create, name='department_create'),
    path('department/<int:pk>/edit/', views.department_edit, name='department_edit'),
    path('department/<int:pk>/delete/', views.department_delete, name='department_delete'),
    path('position/create/', views.position_create, name='position_create'),
    path('position/<int:pk>/edit/', views.position_edit, name='position_edit'),
    path('position/<int:pk>/delete/', views.position_delete, name='position_delete'),
    # 员工创建URL员工添加URL
    path('staff/create/', views.staff_create, name='staff_create'),
    # 员工编辑URL
    path('staff/<int:pk>/edit/', views.staff_edit, name='staff_edit'),
    # 员工删除URL
    path('staff/<int:pk>/delete/', views.staff_delete, name='staff_delete'),
    # 项目方案列表URL
    path('project_orders/', views.project_order_list, name='project_order_list'),
    # 获取客户订单API
    path('api/client_orders/', views.get_client_orders, name='get_client_orders'),
    # 项目方案添加URL
    path('project_orders/create/', views.project_order_create, name='project_order_create'),
    # 项目方案详情URL
    path('project_orders/<int:pk>/', views.project_order_detail, name='project_order_detail'),
    path('project_orders/by-id/<str:project_id>/', views.project_order_detail_by_id, name='project_order_detail_by_id'),
    # 项目方案编辑URL
    path('project_orders/<int:pk>/edit/', views.project_order_edit, name='project_order_edit'),
    # 项目方案删除URL
    path('project_orders/<int:pk>/delete/', views.project_order_delete, name='project_order_delete'),
    # 报告列表URL
    path('reports/', views.report_list, name='report_list'),
    # 报告添加URL
    path('reports/create/', views.report_create, name='report_create'),
    # 报告编辑URL
    path('reports/<int:pk>/edit/', views.report_edit, name='report_edit'),
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
    # 样品类型描述列表URL
    path('sample_type_descriptions/', views.sample_type_description_list, name='sample_type_description_list'),
    # 样品类型描述添加URL
    path('sample_type_descriptions/create/', views.sample_type_description_create, name='sample_type_description_create'),
    # 样品类型描述编辑URL
    path('sample_type_descriptions/<int:pk>/edit/', views.sample_type_description_edit, name='sample_type_description_edit'),
    # 样品类型描述删除URL
    path('sample_type_descriptions/<int:pk>/delete/', views.sample_type_description_delete, name='sample_type_description_delete'),
    # 样品类型列表URL
    path('sample_types/', views.sample_type_list, name='sample_type_list'),
    # 样品类型添加URL
    path('sample_types/create/', views.sample_type_create, name='sample_type_create'),
    # 样品类型编辑URL
    path('sample_types/<int:pk>/edit/', views.sample_type_edit, name='sample_type_edit'),
    # 样品类型删除URL
    path('sample_types/<int:pk>/delete/', views.sample_type_delete, name='sample_type_delete'),
    # 测试Excel批量导入URL
    path('tests/import_excel/', views.test_import_excel, name='test_import_excel'),
    # 测试Excel导入模板下载URL
    path('tests/import_template/', views.test_import_template, name='test_import_template'),
    # 保存辐射测量信息 URL
    path('tests/save_radiation_info/', views.save_radiation_info, name='save_radiation_info'),
    
    # 导入模板管理URL
    path('import_templates/', views.import_template_list, name='import_template_list'),
    path('import_templates/create/', views.import_template_create, name='import_template_create'),
    path('import_templates/<int:template_id>/edit/', views.import_template_edit, name='import_template_edit'),
    path('import_templates/<int:template_id>/delete/', views.import_template_delete, name='import_template_delete'),
    path('import_templates/<int:template_id>/download/', views.import_template_download, name='import_template_download'),
    
]