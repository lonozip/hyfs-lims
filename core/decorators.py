from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from .models import Staff

def require_permission(permission_name):
    """
    装饰器：检查员工是否具有指定权限
    :param permission_name: 权限名称（如 'can_manage_clients'）
    """
    def decorator(view_func):
        def wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            
            try:
                staff = Staff.objects.get(user=request.user)
                # 检查是否具有指定权限
                if not getattr(staff, permission_name, False):
                    return HttpResponseForbidden('您没有访问此页面的权限')
            except Staff.DoesNotExist:
                return HttpResponseForbidden('您没有访问此页面的权限')
            
            return view_func(request, *args, **kwargs)
        return wrapped_view
    return decorator
