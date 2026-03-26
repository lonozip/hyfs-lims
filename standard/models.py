from django.db import models
from django.contrib.auth.models import User


class StandardLibrary(models.Model):
    """标准库模型"""
    # 标准库名称
    name = models.CharField(max_length=255, verbose_name='标准库名称')
    # 标准库描述
    description = models.TextField(blank=True, verbose_name='标准库描述')
    # 创建人
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='创建人')
    # 创建时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # 更新时间
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '标准库'
        verbose_name_plural = '标准库'
    
    def __str__(self):
        return self.name

class Standard_radiation_hygiene(models.Model):
    """标准模型"""
    # 标准状态选项                                
    STATUS_CHOICES = [
        ('pending', '待实行'),
        ('in_progress', '试行中'),
        ('completed', '已实行'),
        ('cancelled', '已取消'),
    ]
    # 关联到标准库
    library = models.ForeignKey(StandardLibrary, on_delete=models.CASCADE, null=True, blank=True, verbose_name='标准库')
    # 标准名称
    name = models.CharField(max_length=255, verbose_name='标准名称')
    # 测试名称
    test_name = models.CharField(max_length=255, default='', verbose_name='测试名称')
    # 测试描述
    description = models.TextField(blank=True, verbose_name='测试描述')
    # 测试单位
    unit = models.CharField(max_length=50, default='', verbose_name='测试单位')
    
    # 验收检测相关字段
    acceptance_reference_range = models.CharField(max_length=100, default='', verbose_name='验收检测参考范围')
    
    # 状态检测相关字段
    status_reference_range = models.CharField(max_length=100, default='', verbose_name='状态检测参考范围')
    
    # 稳定性检测相关字段
    stability_reference_range = models.CharField(max_length=100, default='', verbose_name='稳定性检测参考范围')
    
    # 标准类型
    standard_type = models.CharField(max_length=255, verbose_name='标准类型')
    # 标准编号
    standard_id = models.CharField(max_length=50, verbose_name='标准编号')
    # 采集日期
    collection_date = models.DateTimeField(verbose_name='采集日期')
    # 标准状态
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    # 创建人
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='创建人')
    # 创建时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # 更新时间
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        """返回标准编号作为字符串表示"""
        return self.standard_id

    class Meta:
        verbose_name = '放射卫生标准'
        verbose_name_plural = '放射卫生标准'


class Standard(models.Model):
    """标准模型"""
    # 放射卫生标准状态选项                                
    STATUS_CHOICES = [
        ('pending', '待实行'),
        ('in_progress', '试行中'),
        ('completed', '已实行'),
        ('cancelled', '已取消'),
    ]
    # 关联到标准库
    library = models.ForeignKey(StandardLibrary, on_delete=models.CASCADE, null=True, blank=True, verbose_name='标准库')
    # 标准名称
    name = models.CharField(max_length=255, verbose_name='标准名称')
    # 测试名称
    test_name = models.CharField(max_length=255, default='', verbose_name='测试名称')
    # 测试描述
    description = models.TextField(blank=True, verbose_name='测试描述')
    # 测试单位
    unit = models.CharField(max_length=50, default='', verbose_name='测试单位')
    
    # 参考范围
    acceptance_reference_range = models.CharField(max_length=100, default='', verbose_name='参考范围')
    
    # 标准类型
    standard_type = models.CharField(max_length=255, verbose_name='标准类型')
    # 标准编号
    standard_id = models.CharField(max_length=50, verbose_name='标准编号')
    # 采集日期
    collection_date = models.DateTimeField(verbose_name='采集日期')
    # 标准状态
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    # 创建人
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='创建人')
    # 创建时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # 更新时间
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        """返回标准编号作为字符串表示"""
        return self.standard_id

    class Meta:
        verbose_name = '标准'
        verbose_name_plural = '标准'