# 导入Django路径函数
from django.urls import path
# 从core应用导入视图模块，因为模型和视图都在core应用中
from core import views

# URL模式列表
urlpatterns = [
    # 样品类型列表URL
    path('', views.sample_type_list, name='sample_type_list'),
    # 样品类型添加URL
    path('create/', views.sample_type_create, name='sample_type_create'),
    # 样品类型编辑URL
    path('<int:pk>/edit/', views.sample_type_edit, name='sample_type_edit'),
    # 样品类型删除URL
    path('<int:pk>/delete/', views.sample_type_delete, name='sample_type_delete'),
    # 样品类型描述列表URL
    path('descriptions/', views.sample_type_description_list, name='sample_type_description_list'),
    # 样品类型描述添加URL
    path('descriptions/create/', views.sample_type_description_create, name='sample_type_description_create'),
    # 样品类型描述编辑URL
    path('descriptions/<int:pk>/edit/', views.sample_type_description_edit, name='sample_type_description_edit'),
    # 样品类型描述删除URL
    path('descriptions/<int:pk>/delete/', views.sample_type_description_delete, name='sample_type_description_delete'),
]
