# 导入Django模型模块
from django.db import models
# 导入Django用户模型
from django.contrib.auth.models import User
# 导入日期时间模块
from datetime import datetime
# 导入os模块
import os

def get_test_image_path(instance, filename):
    """
    生成测试图片的存储路径
    """
    # 获取文件扩展名
    ext = filename.split('.')[-1]
    # 生成新的文件名
    new_filename = f"test_{instance.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"
    # 返回存储路径
    return os.path.join('test_images', new_filename)


def get_import_template_path(instance, filename):
    """
    生成导入模板文件的存储路径
    """
    # 获取文件扩展名
    ext = filename.split('.')[-1]
    # 生成新的文件名
    new_filename = f"template_{instance.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"
    # 返回存储路径
    return os.path.join('import_templates', new_filename)


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
    # 省份
    province = models.CharField(max_length=100, blank=True, default='', verbose_name='省份')
    # 城市
    city = models.CharField(max_length=100, blank=True, default='', verbose_name='城市')

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


class SampleTypeDescription(models.Model):
    """样品类型描述模型"""
    # 关联的样品类型
    sample_type = models.ForeignKey(SampleType, on_delete=models.CASCADE, verbose_name='样品类型')
    # 描述内容
    description = models.TextField(blank=True, verbose_name='描述内容')
    # 量纲（显示用）
    unit = models.CharField(max_length=50, blank=True, verbose_name='量纲')
    # 基础单位（用于换算）
    base_unit = models.CharField(max_length=50, blank=True, verbose_name='基础单位')
    # 创建人
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='创建人')
    # 创建时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # 更新时间
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        """返回样品类型描述作为字符串表示"""
        return self.description

    def get_converted_unit(self, target_prefix):
        """
        将基础单位转换为目标数量级
        :param target_prefix: 目标数量级前缀
        :return: 转换后的单位字符串
        """
        from .unit_converter import format_unit
        return format_unit(target_prefix, self.base_unit)

    class Meta:
        verbose_name = '样品类型描述'
        verbose_name_plural = '样品类型描述'


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
    # 关联的方案
    project_order = models.ForeignKey('Project_Order', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='方案', related_name='samples')
    # 样品类型
    sample_type = models.ForeignKey(SampleType, on_delete=models.SET_NULL, null=True, verbose_name='样品类型')
    # 样品类型描述
    sample_type_description = models.ForeignKey(SampleTypeDescription, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='样品类型描述')
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
    # 测试状态
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    # 测试结果
    result = models.CharField(max_length=100, blank=True, verbose_name='测试结果')
    # 量纲（显示用）
    unit = models.CharField(max_length=50, blank=True, verbose_name='量纲')
    # 基础单位（用于换算）
    base_unit = models.CharField(max_length=50, blank=True, verbose_name='基础单位')
    # 基础值（存储基础单位下的值）
    base_value = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True, verbose_name='基础值')
    # 分析人员
    analyzed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='analyzed_tests', verbose_name='分析人员')
    # 验证人员
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_tests', verbose_name='验证人员')
    # 分析日期
    analysis_date = models.DateTimeField(null=True, blank=True, verbose_name='分析日期')
    # 验证日期
    verification_date = models.DateTimeField(null=True, blank=True, verbose_name='验证日期')
    # 地址信息
    address = models.TextField(blank=True, verbose_name='地址信息')
    # 现场数据
    field_data = models.TextField(blank=True, verbose_name='现场数据')
    # 测试照片
    photo = models.ImageField(upload_to=get_test_image_path, blank=True, null=True, verbose_name='测试照片')
    
    # 辐射剂量率专用字段
    # 点位描述
    point_description = models.CharField(max_length=255, blank=True, verbose_name='点位描述')
    # 经度（E）
    longitude = models.DecimalField(max_digits=15, decimal_places=10, null=True, blank=True, verbose_name='经度（E）')
    # 纬度（N）
    latitude = models.DecimalField(max_digits=15, decimal_places=10, null=True, blank=True, verbose_name='纬度（N）')
    # 高程（H）
    elevation = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='高程（H）')
    # 仪器示值Rγ(1-10)
    r_gamma_1 = models.FloatField(null=True, blank=True, verbose_name='仪器示值Rγ(1)')
    r_gamma_2 = models.FloatField(null=True, blank=True, verbose_name='仪器示值Rγ(2)')
    r_gamma_3 = models.FloatField(null=True, blank=True, verbose_name='仪器示值Rγ(3)')
    r_gamma_4 = models.FloatField(null=True, blank=True, verbose_name='仪器示值Rγ(4)')
    r_gamma_5 = models.FloatField(null=True, blank=True, verbose_name='仪器示值Rγ(5)')
    r_gamma_6 = models.FloatField(null=True, blank=True, verbose_name='仪器示值Rγ(6)')
    r_gamma_7 = models.FloatField(null=True, blank=True, verbose_name='仪器示值Rγ(7)')
    r_gamma_8 = models.FloatField(null=True, blank=True, verbose_name='仪器示值Rγ(8)')
    r_gamma_9 = models.FloatField(null=True, blank=True, verbose_name='仪器示值Rγ(9)')
    r_gamma_10 = models.FloatField(null=True, blank=True, verbose_name='仪器示值Rγ(10)')
    # 宇宙射线
    cosmic_ray = models.FloatField(null=True, blank=True, verbose_name='宇宙射线')
    # k3
    k3 = models.FloatField(null=True, blank=True, verbose_name='k3')
    # 平均值
    avg_value = models.FloatField(null=True, blank=True, verbose_name='平均值')
    # 标准差
    std_value = models.FloatField(null=True, blank=True, verbose_name='标准差')
    # 备注
    remark = models.TextField(blank=True, verbose_name='备注')
    
    # 创建时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # 更新时间
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        """返回样品编号和状态作为字符串表示"""
        return f"{self.sample.sample_id} - {self.get_status_display()}"

    def convert_to_unit(self, target_unit):
        """
        将基础值转换为目标单位的值
        :param target_unit: 目标单位字符串
        :return: 转换后的值
        """
        from .unit_converter import convert_from_base_unit
        if self.base_value is not None and self.base_unit:
            return convert_from_base_unit(self.base_value, target_unit)
        return None

    def convert_from_unit(self, value, source_unit):
        """
        将指定单位的值转换为基础单位值
        :param value: 原始值
        :param source_unit: 原始单位
        :return: 基础单位下的值
        """
        from .unit_converter import convert_to_base_unit
        base_value, base_unit = convert_to_base_unit(value, source_unit)
        return base_value

    def set_result_with_unit(self, value, unit):
        """
        设置测试结果和单位，同时计算并存储基础值
        :param value: 测试结果值
        :param unit: 单位字符串
        """
        from .unit_converter import convert_to_base_unit, parse_unit
        
        self.result = str(value) if value else ''
        self.unit = unit
        
        if value and unit:
            base_value, base_unit = convert_to_base_unit(value, unit)
            self.base_value = base_value
            self.base_unit = base_unit
        else:
            self.base_value = None
            self.base_unit = ''

    def get_converted_result(self, target_unit):
        """
        获取转换到目标单位的测试结果
        :param target_unit: 目标单位字符串
        :return: (转换后的值, 目标单位)
        """
        from .unit_converter import convert_from_base_unit
        
        if self.base_value is not None and self.base_unit:
            converted_value = convert_from_base_unit(self.base_value, target_unit)
            if converted_value is not None:
                return (converted_value, target_unit)
        return (self.result, self.unit)

    def get_auto_best_display(self):
        """
        自动选择最佳单位进行显示
        :return: (格式化后的字符串, 最佳单位)
                 例如: ('1.23', 'μGy/h') 或 ('123', 'nGy/h')
        """
        from .unit_converter import auto_best_unit, convert_to_base_unit

        if self.base_value is not None and self.base_unit:
            _, display_value, display_unit = auto_best_unit(
                float(self.base_value), self.base_unit
            )
            abs_dv = abs(display_value)
            if abs_dv >= 100:
                formatted = '{:.0f}'.format(display_value)
            elif abs_dv >= 10:
                formatted = '{:.1f}'.format(display_value)
            elif abs_dv >= 1:
                formatted = '{:.2f}'.format(display_value)
            elif abs_dv >= 0.1:
                formatted = '{:.2f}'.format(display_value)
            else:
                formatted = '{:.3f}'.format(display_value)
            return (formatted, display_unit)
        if self.result and self.unit:
            base_value, base_unit = convert_to_base_unit(self.result, self.unit)
            if base_value is not None:
                _, display_value, display_unit = auto_best_unit(base_value, base_unit)
                abs_dv = abs(display_value)
                if abs_dv >= 100:
                    formatted = '{:.0f}'.format(display_value)
                elif abs_dv >= 10:
                    formatted = '{:.1f}'.format(display_value)
                elif abs_dv >= 1:
                    formatted = '{:.2f}'.format(display_value)
                elif abs_dv >= 0.1:
                    formatted = '{:.2f}'.format(display_value)
                else:
                    formatted = '{:.3f}'.format(display_value)
                return (formatted, display_unit)
        return (self.result, self.unit)

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


class Position(models.Model):
    """职务模型"""
    # 职务名称
    name = models.CharField(max_length=255, verbose_name='职务名称')
    # 职务描述
    description = models.TextField(blank=True, verbose_name='职务描述')
    # 创建人
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='创建人')
    # 创建时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # 更新时间
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        """返回职务名称作为字符串表示"""
        return self.name

    class Meta:
        verbose_name = '职务'
        verbose_name_plural = '职务'


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
    # 职务 (旧的字符串字段)
    position = models.CharField(max_length=255, default='', verbose_name='职务(旧)')
    # 职务 (新的模型关联)
    position_link = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='职务')
    
    # 关联的用户账号
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='关联用户')
    # 是否启用登录
    is_active = models.BooleanField(default=False, verbose_name='启用登录')
    # 权限设置
    can_manage_clients = models.BooleanField(default=False, verbose_name='客户管理')
    can_manage_orders = models.BooleanField(default=False, verbose_name='订单管理')
    can_manage_projects = models.BooleanField(default=False, verbose_name='方案管理')
    can_manage_samples = models.BooleanField(default=False, verbose_name='样本管理')
    can_manage_tests = models.BooleanField(default=False, verbose_name='测试管理')
    can_manage_reports = models.BooleanField(default=False, verbose_name='报告管理')
    can_manage_staff = models.BooleanField(default=False, verbose_name='员工管理')
    can_manage_standard = models.BooleanField(default=False, verbose_name='标准管理')
    can_manage_org = models.BooleanField(default=False, verbose_name='组织架构')
    can_manage_sample_types = models.BooleanField(default=False, verbose_name='样品类型管理')
    can_manage_sample_descriptions = models.BooleanField(default=False, verbose_name='样品类型描述')
    can_access_admin = models.BooleanField(default=False, verbose_name='管理后台')
    
    # 创建人
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_staff', verbose_name='创建人')
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
    # 关联的样品类型
    sample_types = models.ManyToManyField(SampleType, verbose_name='样品类型')
    # 关联的样品类型描述
    sample_type_descriptions = models.ManyToManyField(SampleTypeDescription, verbose_name='样品类型描述')
    # 样品描述数量（JSON格式存储）
    sample_type_description_quantities = models.JSONField(default=dict, blank=True, verbose_name='样品描述数量')
    # 关联的标准
    standards = models.ManyToManyField('standard.Standard_radiation_hygiene', verbose_name='标准', related_name='project_order_standards')
    
    # 辐射测量基本信息（用于 X、γ辐射剂量率测量）
    radiation_project_name = models.CharField(max_length=255, blank=True, verbose_name='项目名称')
    radiation_monitoring_date = models.CharField(max_length=50, blank=True, verbose_name='监测日期')
    radiation_location = models.CharField(max_length=255, blank=True, verbose_name='监测地点')
    radiation_weather = models.CharField(max_length=100, blank=True, verbose_name='天气状况')
    radiation_basis = models.CharField(max_length=255, blank=True, verbose_name='监测依据')
    radiation_temperature = models.CharField(max_length=20, blank=True, verbose_name='温度')
    radiation_humidity = models.CharField(max_length=20, blank=True, verbose_name='湿度')
    radiation_conditions = models.TextField(blank=True, verbose_name='测量工况')
    
    # 宇宙射线信息（JSON 格式存储）
    cosmic_ray_info = models.JSONField(default=list, blank=True, verbose_name='宇宙射线信息')
    
    # 仪器信息（JSON 格式存储）
    instrument_info = models.JSONField(default=list, blank=True, verbose_name='仪器信息')
    
    def save(self, *args, **kwargs):
        """重写 save 方法，自动生成方案编号"""
        if not self.project_id:  # 只有在创建新对象时才生成编号
            self.project_id = generate_unique_code('PROJECT', Project_Order, 'project_id')
        super().save(*args, **kwargs)
    
    def __str__(self):
        """返回方案名称作为字符串表示"""
        return self.name

    class Meta:
        verbose_name = '方案'
        verbose_name_plural = '方案'
        indexes = [
            models.Index(fields=['project_id'], name='idx_project_order_project_id'),
            models.Index(fields=['status'], name='idx_project_order_status'),
            models.Index(fields=['created_at'], name='idx_project_order_created_at'),
            models.Index(fields=['client'], name='idx_project_order_client'),
            models.Index(fields=['order'], name='idx_project_order_order'),
        ]


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
    # 关联的标准
    standards = models.ManyToManyField('standard.Standard_radiation_hygiene', verbose_name='标准', related_name='report_standards')
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


class ImportTemplate(models.Model):
    """导入模板模型"""
    # 模板名称
    name = models.CharField(max_length=255, verbose_name='模板名称')
    # 关联的样品类型描述
    sample_type_description = models.ForeignKey(
        SampleTypeDescription, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name='样品类型描述'
    )
    # 模板文件
    template_file = models.FileField(upload_to=get_import_template_path, verbose_name='模板文件')
    # 模板描述
    description = models.TextField(blank=True, verbose_name='模板描述')
    # 是否启用
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    # 创建人
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='创建人')
    # 创建时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # 更新时间
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        """返回模板名称作为字符串表示"""
        return self.name

    class Meta:
        verbose_name = '导入模板'
        verbose_name_plural = '导入模板'