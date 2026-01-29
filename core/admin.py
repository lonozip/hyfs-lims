# 导入Django admin模块
from django.contrib import admin
# 导入所有模型
from .models import Client, Order, Sample, SampleType, Test, Instrument, Standard, Staff, Project_Order, Report, Department

class ClientAdmin(admin.ModelAdmin):
    """客户模型的Admin配置"""
    # 列表页面显示的字段
    list_display = ('name', 'contact_person', 'email', 'phone')
    # 搜索字段
    search_fields = ('name', 'contact_person', 'email')


class SampleTypeAdmin(admin.ModelAdmin):
    """样品类型模型的Admin配置"""
    # 列表页面显示的字段
    list_display = ('name', 'description')
    # 搜索字段
    search_fields = ('name',)


class OrderAdmin(admin.ModelAdmin):
    """订单模型的Admin配置"""
    # 列表页面显示的字段
    list_display = ('name', 'order_id', 'client', 'description')
    # 搜索字段
    search_fields = ('name', 'order_id')
    # 列表过滤器
    list_filter = ('client',)
    # 只读字段
    readonly_fields = ('order_id',)


class SampleAdmin(admin.ModelAdmin):
    """样品模型的Admin配置"""
    # 列表页面显示的字段
    list_display = ('sample_id', 'client', 'order', 'get_order_id', 'sample_type', 'status', 'collection_date', 'received_date')
    # 列表过滤器
    list_filter = ('status', 'client', 'order', 'sample_type')
    # 搜索字段
    search_fields = ('sample_id', 'client__name', 'order__order_id')
    # 只读字段
    readonly_fields = ('sample_id', 'received_date')
    # 编辑页面显示的字段
    fields = ('client', 'order', 'sample_type', 'status', 'collection_date', 'sample_id', 'received_date')
    # 添加媒体资源
    class Media:
        js = ('https://code.jquery.com/jquery-3.6.0.min.js', '/static/core/admin/js/filter_orders.js')
    
    def get_order_id(self, obj):
        """获取订单编号"""
        return obj.order.order_id if obj.order else '无订单'
    get_order_id.short_description = '订单编号'


# TestTypeAdmin已合并到StandardAdmin中
# class TestTypeAdmin(admin.ModelAdmin):
#     """测试类型模型的Admin配置"""
#     # 列表页面显示的字段
#     list_display = ('name', 'unit', 'reference_range')
#     # 搜索字段
#     search_fields = ('name',)


class TestAdmin(admin.ModelAdmin):
    """测试记录模型的Admin配置"""
    # 列表页面显示的字段
    list_display = ('sample', 'test_type', 'status', 'result', 'analyzed_by', 'verified_by')
    # 列表过滤器
    list_filter = ('status', 'test_type', 'analyzed_by', 'verified_by')
    # 搜索字段
    search_fields = ('sample__sample_id', 'test_type__test_name')


class InstrumentAdmin(admin.ModelAdmin):
    """仪器设备模型的Admin配置"""
    # 列表页面显示的字段
    list_display = ('name', 'model', 'serial_number', 'location', 'next_calibration_date')
    # 搜索字段
    search_fields = ('name', 'model', 'serial_number')

###########

class ReportAdmin(admin.ModelAdmin):
    """报告模型的Admin配置"""
    # 列表页面显示的字段
    list_display = ('report_id', 'project_order', 'status', 'created_at', 'updated_at')
    # 列表过滤器
    list_filter = ('status', 'project_order')
    # 搜索字段
    search_fields = ('report_id', 'project_order__name')
    # 只读字段
    readonly_fields = ('report_id',)
    # 多对多字段显示为并排选择列表
    filter_horizontal = ('staff', 'samples', 'test_types', 'standards')



class StandardAdmin(admin.ModelAdmin):
    """标准模型的Admin配置 - 合并了测试类型的功能"""
    # 列表页面显示的字段
    list_display = ('standard_id', 'standard_type', 'test_name', 'unit', 'reference_range', 'status', 'collection_date', 'created_at', 'updated_at')
    # 列表过滤器
    list_filter = ('status', 'standard_type')
    # 搜索字段
    search_fields = ('standard_id', 'standard_type', 'test_name', 'name')


class StaffAdmin(admin.ModelAdmin):
    """员工模型的Admin配置"""
    # 列表页面显示的字段
    list_display = ('staff_id', 'name', 'department', 'email', 'phone', 'address', 'created_by', 'created_at', 'updated_at')
    # 搜索字段
    search_fields = ('name', 'department', 'email', 'phone', 'staff_id')
    # 列表过滤器
    list_filter = ('department',)
    # 只读字段
    readonly_fields = ('staff_id',)

class ProjectOrderAdmin(admin.ModelAdmin):
    """方案模型的Admin配置"""
    # 列表页面显示的字段
    list_display = ('project_id', 'name', 'client', 'order', 'status', 'created_at', 'updated_at', 'created_by')
    # 列表过滤器
    list_filter = ('status', 'client')
    # 搜索字段
    search_fields = ('project_id', 'name', 'client__name')
    # 只读字段
    readonly_fields = ('project_id',)
    # 多对多字段显示为并排选择列表
    filter_horizontal = ('staff', 'samples', 'test_types', 'standards')
    # 添加媒体资源
    class Media:
        js = ('https://code.jquery.com/jquery-3.6.0.min.js', '/static/core/admin/js/filter_orders.js')


class DepartmentAdmin(admin.ModelAdmin):
    """部门模型的Admin配置"""
    # 列表页面显示的字段
    list_display = ('name', 'description', 'created_by')
    # 搜索字段
    search_fields = ('name', 'description')
    # 只读字段
    # readonly_fields = ('created_by',)

# 注册模型到admin后台
admin.site.register(Client, ClientAdmin)
admin.site.register(SampleType, SampleTypeAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Sample, SampleAdmin)
admin.site.register(Department, DepartmentAdmin)
# TestType模型已合并到Standard模型中，不再需要单独注册
# admin.site.register(TestType, TestTypeAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(Instrument, InstrumentAdmin)
admin.site.register(Standard, StandardAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(Project_Order, ProjectOrderAdmin)
admin.site.register(Report, ReportAdmin)
