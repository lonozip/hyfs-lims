"""
URL configuration for senaite_lims project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf import settings
from django.conf.urls.static import static
from core import views

# 简单的测试视图
from django.http import HttpResponse
def test_view(request):
    return HttpResponse('Hello, World!')

urlpatterns = [
    path('admin/', admin.site.urls),
    # 测试视图URL
    path('test/', test_view, name='test_view'),
    path('login/', views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
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
    # 其他URL
    path('', include('core.urls')),
    path('standard/', include('standard.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
