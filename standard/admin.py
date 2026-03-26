from django.contrib import admin
from .models import StandardLibrary, Standard, Standard_radiation_hygiene
from .forms import StandardForm


class StandardLibraryAdmin(admin.ModelAdmin):
    """标准库模型的Admin配置"""
    # 列表页面显示的字段
    list_display = ('name', 'description', 'created_by', 'created_at', 'updated_at')
    # 搜索字段
    search_fields = ('name', 'description')


class StandardAdmin(admin.ModelAdmin):
    """标准模型的Admin配置"""
    # 列表页面显示的字段
    list_display = ('standard_id', 'library', 'standard_type', 'test_name', 'unit', 'status', 'collection_date', 'created_at', 'updated_at')
    # 列表过滤器
    list_filter = ('status', 'standard_type', 'library')
    # 搜索字段
    search_fields = ('standard_id', 'standard_type', 'test_name', 'name', 'library__name')
    # 使用自定义表单
    form = StandardForm
    
    # 添加媒体资源
    class Media:
        js = ('https://code.jquery.com/jquery-3.6.0.min.js',)
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
    
    # 自定义模板
    change_form_template = 'admin/standard/standard_change_form.html'

class Standard_radiation_hygieneAdmin(admin.ModelAdmin):
    """放射卫生标准模型的Admin配置"""
    # 列表页面显示的字段
    list_display = ('standard_id', 'library', 'name', 'test_name', 'unit', 'collection_date', 'created_at', 'updated_at')
    # 列表过滤器
    list_filter = ('library',)
    # 搜索字段
    search_fields = ('standard_id', 'library__name', 'name', 'test_name')

# 注册模型到admin后台
admin.site.register(StandardLibrary, StandardLibraryAdmin)
admin.site.register(Standard_radiation_hygiene, StandardAdmin)
admin.site.register(Standard, Standard_radiation_hygieneAdmin)
