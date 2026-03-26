from django.urls import path
from . import views

app_name = 'standard'

urlpatterns = [
    path('libraries/', views.standard_library_list, name='library_list'),
    path('libraries/<int:pk>/', views.standard_library_detail, name='library_detail'),
    path('', views.standard_list, name='standard_list'),
    path('<int:pk>/', views.standard_detail, name='standard_detail'),
]