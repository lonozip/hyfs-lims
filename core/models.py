# 导入Django模型模块
from django.db import models
# 导入Django用户模型
from django.contrib.auth.models import User
# 导入日期时间模块
from datetime import datetime


def generate_unique_code(prefix, model_class, field_name, date_format='%Y%m%d', seq_length=4):
    """
    生成基于时间日期的唯一编号
    
    参数：
    - prefix: 编号前缀（如'STAFF'、'SAMPLE'）
    - model_class: 模型类
    - field_name: 字段名称
    - date_format: 日期格式
    - seq_length: 序号长度
    
    返回：
    - 唯一编号字符串
    """
    # 获取当前日期
    current_date = datetime.now().strftime(date_format)
    # 构造查询前缀
    code_prefix = f'{prefix}-{current_date}-'
    
    # 计算当天已存在的记录数量
    query_params = {f'{field_name}__startswith': code_prefix}
    today_count = model_class.objects.filter(**query_params).count()
    
    # 生成序号
    seq = str(today_count + 1).zfill(seq_length)
    
    # 构造完整编号
    return f'{code_prefix}{seq}'


class Client(models.Model):
    """客户模型"""
    # 客户名称
    name = models.CharField(max_length=255, verbose_name='客户名称')
    # 联系人
    contact_person = models.CharField(max_length=255, verbose_name='联系人')
    # 邮箱
    email = models.EmailField(verbose_name='电子邮件')
    # 电话号码
    phone = models.CharField(max_length=20, verbose_name='电话')
    # 地址
    address = models.TextField(verbose_name='地址')
    # 创建人
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='创建人')
    # 创建时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # 更新时间
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        """返回客户名称作为字符串表示"""
        return self.name

    class Meta:
        verbose_name = '客户'
        verbose_name_plural = '客户'


class SampleType(models.Model):
    """样品类型模型"""
    # 类型名称
    name = models.CharField(max_length=255, verbose_name='类型名称')
    # 类型描述
    description = models.TextField(blank=True, verbose_name='类型描述')
    # 创建人
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='创建人')
    # 创建时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # 更新时间
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        """返回样品类型名称作为字符串表示"""
        return self.name

    class Meta:
        verbose_name = '样品类型'
        verbose_name_plural = '样品类型'


class Order(models.Model):
    """订单模型"""
    # 订单状态选项
    STATUS_CHOICES = [
        ('pending', '待处理'),
        ('in_progress', '处理中'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    ]
    #订单编号
    order_id = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name='订单编号')
    # 订单名称
    name = models.CharField(max_length=255, verbose_name='订单名称')
    # 订单描述
    description = models.TextField(blank=True, verbose_name='订单描述')
    # 关联的客户
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='客户')
    # 订单状态
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='订单状态')
    # 创建人
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='创建人')
    # 创建时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # 更新时间
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    def save(self, *args, **kwargs):
        """重写save方法，自动生成订单编号"""
        if not self.order_id:  # 只有在创建新对象时才生成编号
            self.order_id = generate_unique_code('ORDER', Order, 'order_id')
        super().save(*args, **kwargs)

    def __str__(self):
        """返回订单名称和编号作为字符串表示"""
        return f"{self.name} (ID: {self.order_id})"

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = '订单'



####
class Sample(models.Model):
    """样品模型"""
    # 样品状态选项
    STATUS_CHOICES = [
        ('pending', '待处理'),
        ('in_progress', '处理中'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    ]

    # 关联的客户
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='客户')
    # 关联的订单
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, verbose_name='订单')
    # 样品类型
    sample_type = models.ForeignKey(SampleType, on_delete=models.SET_NULL, null=True, verbose_name='样品类型')
    # 样品编号
    sample_id = models.CharField(max_length=50, unique=True, verbose_name='样品编号')
    # 采集日期
    collection_date = models.DateTimeField(verbose_name='采集日期')
    # 接收日期
    received_date = models.DateTimeField(auto_now_add=True, verbose_name='接收日期')
    # 样品状态
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    # 创建人
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='创建人')
    # 创建时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # 更新时间
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    def save(self, *args, **kwargs):
        """重写save方法，自动生成样品编号"""
        if not self.sample_id:  # 只有在创建新对象时才生成编号
            self.sample_id = generate_unique_code('SAMPLE', Sample, 'sample_id')
        super().save(*args, **kwargs)

    def __str__(self):
        """返回样品编号作为字符串表示"""
        return self.sample_id

    class Meta:
        verbose_name = '样品'
        verbose_name_plural = '样品'


# TestType模型已合并到Standard模型中
# class TestType(models.Model):
#     """测试类型模型"""
#     # 测试名称
#     name = models.CharField(max_length=255, verbose_name='测试名称')
#     # 测试描述
#     description = models.TextField(blank=True, verbose_name='测试描述')
#     # 测试单位
#     unit = models.CharField(max_length=50, verbose_name='测试单位')
#     # 参考范围
#     reference_range = models.CharField(max_length=100, verbose_name='参考范围')
#     # 创建人
#     created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='创建人')
#     # 创建时间
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
#     # 更新时间
#     updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
#
#     def __str__(self):
#         """返回测试类型名称作为字符串表示"""
#         return self.name
#
#     class Meta:
#         verbose_name = '测试类型'
#         verbose_name_plural = '测试类型'


class Test(models.Model):
    """测试记录模型"""
    # 测试状态选项
    STATUS_CHOICES = [
        ('pending', '待测试'),
        ('in_progress', '测试中'),
        ('completed', '已完成'),
        ('failed', '测试失败'),
    ]

    # 关联的样品
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE, verbose_name='样品')
    # 测试类型（现在关联到Standard模型）
    test_type = models.ForeignKey('standard.Standard', on_delete=models.CASCADE, verbose_name='测试类型')
    # 测试状态
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    # 测试结果
    result = models.CharField(max_length=100, blank=True, verbose_name='测试结果')
    # 分析人员
    analyzed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='analyzed_tests', verbose_name='分析人员')
    # 验证人员
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_tests', verbose_name='验证人员')
    # 分析日期
    analysis_date = models.DateTimeField(null=True, blank=True, verbose_name='分析日期')
    # 验证日期
    verification_date = models.DateTimeField(null=True, blank=True, verbose_name='验证日期')
    # 创建时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # 更新时间
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        """返回样品编号和测试类型作为字符串表示"""
        return f"{self.sample.sample_id} - {self.test_type.test_name}"

    class Meta:
        verbose_name = '测试记录'
        verbose_name_plural = '测试记录'


class Instrument(models.Model):
    """仪器设备模型"""
    # 仪器名称
    name = models.CharField(max_length=255, verbose_name='仪器名称')
    # 仪器型号
    model = models.CharField(max_length=255, verbose_name='仪器型号')
    # 序列号
    serial_number = models.CharField(max_length=100, verbose_name='序列号')
    # 存放位置
    location = models.CharField(max_length=255, verbose_name='存放位置')
    # 校准日期
    calibration_date = models.DateTimeField(null=True, blank=True, verbose_name='校准日期')
    # 下次校准日期
    next_calibration_date = models.DateTimeField(null=True, blank=True, verbose_name='下次校准日期')
    # 创建人
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='创建人')
    # 创建时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # 更新时间
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        """返回仪器名称作为字符串表示"""
        return self.name

    class Meta:
        verbose_name = '仪器设备'
        verbose_name_plural = '仪器设备'




class Department(models.Model):
    """部门模型"""
    # 部门名称
    name = models.CharField(max_length=255, verbose_name='部门名称')
    # 部门描述
    description = models.TextField(blank=True, verbose_name='部门描述') 
    # 创建人
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='创建人')

    def __str__(self):
        """返回部门名称作为字符串表示"""
        return self.name

    class Meta:
        verbose_name = '部门'
        verbose_name_plural = '部门'


class Staff(models.Model):
    """员工模型"""
    # 员工id
    id = models.AutoField(primary_key=True)
    # 员工编号 - 自动生成唯一编号
    staff_id = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name='员工编号')
    
    # 员工姓名
    name = models.CharField(max_length=255, verbose_name='员工姓名')
    
    # 联系人
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, verbose_name='部门')
    # 邮箱
    email = models.EmailField(verbose_name='电子邮件')
    # 电话号码
    phone = models.CharField(max_length=20, verbose_name='电话')
    # 地址
    address = models.TextField(verbose_name='地址')
    # 创建人
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='创建人')
    # 创建时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # 更新时间
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    def save(self, *args, **kwargs):
        """重写save方法，自动生成员工编号"""
        if not self.staff_id:  # 只有在创建新对象时才生成编号
            self.staff_id = generate_unique_code('STAFF', Staff, 'staff_id')
        super().save(*args, **kwargs)

    def __str__(self):
        """返回员工姓名作为字符串表示"""
        return self.name

    class Meta:
        verbose_name = '员工'
        verbose_name_plural = '员工'


class Project_Order(models.Model):
    """方案模型"""
    # 方案状态选项
    STATUS_CHOICES = [
        ('pending', '待处理'),
        ('in_progress', '处理中'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    ]
    
    # 方案编号
    project_id = models.CharField(max_length=50, unique=True, verbose_name='方案编号')
    # 方案名称
    name = models.CharField(max_length=255, verbose_name='方案名称')
    # 方案描述
    description = models.TextField(blank=True, verbose_name='方案描述')
    # 关联的客户
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='客户')
    # 关联的订单
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='订单')
    # 方案状态
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='方案状态')
    # 创建人
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_project_orders', verbose_name='创建人')
    # 创建时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # 更新时间
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    # 关联的员工
    staff = models.ManyToManyField(Staff, verbose_name='员工', related_name='assigned_project_orders')
    # 关联的样品
    samples = models.ManyToManyField(Sample, verbose_name='样品')
    # 关联的测试类型（现在关联到Standard模型）
    test_types = models.ManyToManyField('standard.Standard', verbose_name='测试类型', related_name='project_order_test_types')
    # 关联的标准
    standards = models.ManyToManyField('standard.Standard_radiation_hygiene', verbose_name='标准', related_name='project_order_standards')
    
    def save(self, *args, **kwargs):
        """重写save方法，自动生成方案编号"""
        if not self.project_id:  # 只有在创建新对象时才生成编号
            self.project_id = generate_unique_code('PROJECT', Project_Order, 'project_id')
        super().save(*args, **kwargs)
    
    def __str__(self):
        """返回方案名称作为字符串表示"""
        return self.name

    class Meta:
        verbose_name = '方案'
        verbose_name_plural = '方案'


class Report(models.Model):
    """报告模型"""
    # 报告状态选项
    STATUS_CHOICES = [
        ('pending', '报告编制'),
        ('in_progress', '报告审核'),
        ('completed', '报告签发'),
        ('cancelled', '报告作废'),
    ]
    # 关联的方案
    project_order = models.ForeignKey(Project_Order, on_delete=models.CASCADE, null=True, blank=True, verbose_name='关联的方案')
    # 报告编号
    report_id = models.CharField(max_length=50, unique=True, verbose_name='报告编号')
    # 报告名称
    name = models.CharField(max_length=255, verbose_name='报告名称')
    # 报告描述
    description = models.TextField(blank=True, verbose_name='报告描述')
    # 关联的客户
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='客户')
    # 关联的订单
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='订单')
    # 报告状态
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='报告状态')
    # 创建人
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_reports', verbose_name='创建人')
    # 创建时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # 更新时间
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    # 关联的员工
    staff = models.ManyToManyField(Staff, verbose_name='员工', related_name='assigned_reports')
    # 关联的样品
    samples = models.ManyToManyField(Sample, verbose_name='样品')
    # 关联的测试类型（现在关联到Standard模型）
    test_types = models.ManyToManyField('standard.Standard', verbose_name='测试类型', related_name='report_test_types')
    # 关联的标准
    standards = models.ManyToManyField('standard.Standard', verbose_name='标准', related_name='report_standards')
    # 关联的测试结果
    test_results = models.ManyToManyField(Test, verbose_name='测试结果', related_name='report_test_results')
    # PDF文件
    pdf_file = models.FileField(upload_to='report_pdfs/', blank=True, null=True, verbose_name='PDF文件')
    
    def save(self, *args, **kwargs):
        """重写save方法，自动生成报告编号"""
        if not self.pk:  # 只有在创建新对象时才生成编号
            from datetime import datetime
            # 获取当前日期
            current_date = datetime.now().strftime('%Y%m%d')
            # 计算当天已存在的报告数量，用于生成序号
            prefix = f'REPORT-{current_date}-'
            # 获取当天报告数量
            today_count = Report.objects.filter(report_id__startswith=prefix).count()
            # 生成报告编号：REPORT-YYYYMMDD-0001
            self.report_id = f'{prefix}{str(today_count + 1).zfill(4)}'
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        """返回方案名称作为字符串表示"""
        return self.name

    class Meta:
        verbose_name = '报告'
        verbose_name_plural = '报告'
        permissions = (
            ('can_approve_report', '可以审核报告'),
            ('can_sign_report', '可以签发报告'),
            ('can_reject_report', '可以拒绝报告'),
        )

