# 导入Django admin模块
from django.contrib import admin
# 导入所有模型
from .models import Client, Order, Sample, SampleType, Test, Instrument, Staff, Project_Order, Report, Department, Position

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
    filter_horizontal = ('staff', 'samples', 'test_results', 'test_types', 'standards')


class PositionAdmin(admin.ModelAdmin):
    """职务模型的Admin配置"""
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name',)

class StaffAdmin(admin.ModelAdmin):
    """员工模型的Admin配置"""
    list_display = ('name', 'staff_id', 'department', 'position_link', 'phone', 'email')
    search_fields = ('name', 'staff_id', 'phone', 'email')
    list_filter = ('department', 'position_link')

class Project_OrderAdmin(admin.ModelAdmin):
    """方案模型的Admin配置"""
    list_display = ('project_id', 'name', 'client', 'order', 'status')
    search_fields = ('project_id', 'name', 'client__name', 'order__order_id')
    list_filter = ('status', 'client')
    readonly_fields = ('project_id',)
    filter_horizontal = ('staff', 'sample_types', 'sample_type_descriptions', 'test_types', 'standards')

class DepartmentAdmin(admin.ModelAdmin):
    """部门模型的Admin配置"""
    list_display = ('name', 'description')
    search_fields = ('name',)

# 注册所有模型
admin.site.register(Client, ClientAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Sample, SampleAdmin)
admin.site.register(SampleType, SampleTypeAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(Instrument, InstrumentAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(Project_Order, Project_OrderAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Position, PositionAdmin)