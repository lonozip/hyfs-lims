from .models import Staff

def staff_permissions(request):
    """上下文处理器：获取当前用户的员工权限"""
    # 默认权限为空
    permissions = {
        'can_manage_clients': False,
        'can_manage_orders': False,
        'can_manage_projects': False,
        'can_manage_samples': False,
        'can_manage_tests': False,
        'can_manage_reports': False,
        'can_manage_staff': False,
        'can_manage_standard': False,
        'can_manage_org': False,
        'can_manage_sample_types': False,
        'can_manage_sample_descriptions': False,
        'can_access_admin': False,
    }
    
    if request.user.is_authenticated:
        try:
            # 获取当前用户关联的员工信息
            staff = Staff.objects.get(user=request.user)
            # 设置权限
            permissions['can_manage_clients'] = staff.can_manage_clients
            permissions['can_manage_orders'] = staff.can_manage_orders
            permissions['can_manage_projects'] = staff.can_manage_projects
            permissions['can_manage_samples'] = staff.can_manage_samples
            permissions['can_manage_tests'] = staff.can_manage_tests
            permissions['can_manage_reports'] = staff.can_manage_reports
            permissions['can_manage_staff'] = staff.can_manage_staff
            permissions['can_manage_standard'] = staff.can_manage_standard
            permissions['can_manage_org'] = staff.can_manage_org
            permissions['can_manage_sample_types'] = staff.can_manage_sample_types
            permissions['can_manage_sample_descriptions'] = staff.can_manage_sample_descriptions
            permissions['can_access_admin'] = staff.can_access_admin
        except Staff.DoesNotExist:
            # 如果没有关联员工，保持默认权限（全部为False）
            pass
    
    return {'staff_permissions': permissions}
