# 导入Django快捷函数
from django.shortcuts import render, get_object_or_404, redirect
# 导入登录验证装饰器
from django.contrib.auth.decorators import login_required
# 导入请求方法装饰器
from django.views.decorators.http import require_GET
# 导入JSON响应模块
from django.http import JsonResponse, HttpResponse
# 导入模型
from .models import Client, Sample, Test, Order, Staff, Project_Order, Report, Department
# 导入standard应用的模型
from standard.models import Standard, StandardLibrary, Standard_radiation_hygiene

# 导入消息框架
from django.contrib import messages
# 导入ORM聚合函数
from django.db.models import Count
# 导入JSON模块
import json
# 导入用户模型和认证相关功能
from django.contrib.auth.models import User
# 导入模板渲染函数
from django.template.loader import render_to_string
# 导入PDF生成库
from weasyprint import HTML
# 导入临时文件和操作系统模块
import tempfile
import os
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


def register(request):
    """用户注册视图函数"""
    if request.method == 'POST':
        # 获取表单数据
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        # 验证密码是否一致
        if password1 != password2:
            messages.error(request, '两次输入的密码不一致')
            return redirect('register')
        
        # 验证用户名是否已存在
        if User.objects.filter(username=username).exists():
            messages.error(request, '用户名已被使用')
            return redirect('register')
        
        # 验证邮箱是否已存在
        if User.objects.filter(email=email).exists():
            messages.error(request, '邮箱已被注册')
            return redirect('register')
        
        # 创建新用户
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        
        # 自动登录新用户
        login(request, user)
        
        # 显示成功消息并跳转首页
        messages.success(request, '注册成功！欢迎使用LIMS系统')
        return redirect('home')
    
    # GET请求时渲染注册页面
    return render(request, 'core/register.html')


@login_required
def home(request):
    """首页视图函数 - 显示系统概览信息和数据可视化"""
    # 获取客户总数
    total_clients = Client.objects.count()
    # 获取样品总数
    total_samples = Sample.objects.count()
    # 获取订单总数
    total_orders = Order.objects.count()
    # 获取待处理测试数量
    pending_tests = Test.objects.filter(status='pending').count()
    # 获取已完成测试数量
    completed_tests = Test.objects.filter(status='completed').count()
    # 获取报告总数
    total_reports = Report.objects.count()
    
    # 统计不同状态的样品数量（用于饼图）
    sample_status_data = Sample.objects.values('status').annotate(count=Count('status'))
    # 准备样品状态饼图数据：标签（状态）和值（数量）
    sample_labels = [item['status'] for item in sample_status_data]
    sample_values = [item['count'] for item in sample_status_data]
    # 将样品状态数据转换为JSON格式（便于前端JavaScript使用）
    sample_chart_data = {
        'labels': sample_labels,
        'values': sample_values
    }
    
    # 统计不同状态的订单数量（用于饼图）
    order_status_data = Order.objects.values('status').annotate(count=Count('status'))
    # 准备订单状态饼图数据：标签（状态）和值（数量）
    order_labels = [item['status'] for item in order_status_data]
    order_values = [item['count'] for item in order_status_data]
    # 将订单状态数据转换为JSON格式（便于前端JavaScript使用）
    order_chart_data = {
        'labels': order_labels,
        'values': order_values
    }
    
    # 统计不同状态的报告数量（用于饼图）
    report_status_data = Report.objects.values('status').annotate(count=Count('status'))
    # 准备报告状态饼图数据：标签（状态）和值（数量）
    report_labels = [item['status'] for item in report_status_data]
    report_values = [item['count'] for item in report_status_data]
    # 将报告状态数据转换为JSON格式（便于前端JavaScript使用）
    report_chart_data = {
        'labels': report_labels,
        'values': report_values
    }
    
    # 准备上下文数据
    context = {
        'total_clients': total_clients,
        'total_samples': total_samples,
        'total_orders': total_orders,
        'pending_tests': pending_tests,
        'completed_tests': completed_tests,
        'total_reports': total_reports,
        'sample_chart_data': json.dumps(sample_chart_data),  # 添加样品状态饼图数据
        'order_chart_data': json.dumps(order_chart_data),     # 添加订单状态饼图数据
        'report_chart_data': json.dumps(report_chart_data)     # 添加报告状态饼图数据
    }
    
    # 渲染首页模板
    return render(request, 'core/home.html', context)


@login_required
def client_list(request):
    """客户列表视图函数"""
    # 获取所有客户
    clients = Client.objects.all()
    # 渲染客户列表模板
    return render(request, 'core/client_list.html', {'clients': clients})


@login_required
def sample_list(request):
    """样品列表视图函数"""
    # 获取所有样品
    samples = Sample.objects.all()
    # 渲染样品列表模板
    return render(request, 'core/sample_list.html', {'samples': samples})


@login_required
def test_list(request):
    """测试列表视图函数"""
    # 获取所有测试记录
    tests = Test.objects.all()
    # 渲染测试列表模板
    return render(request, 'core/test_list.html', {'tests': tests})

@login_required
def order_list(request):
    """订单列表视图函数"""
    # 获取所有订单
    orders = Order.objects.all()
    # 渲染订单列表模板
    return render(request, 'core/order_list.html', {'orders': orders})
    



# 员工列表视图函数
@login_required
def staff_list(request):
    """员工列表视图函数"""
    # 获取所有员工
    staffs = Staff.objects.all()
    # 渲染员工列表模板
    return render(request, 'core/staff.html', {'staffs': staffs})

#方案订单列表视图函数
@login_required
def project_order_list(request):
    """项目方案订单列表视图函数"""
    # 获取所有项目方案订单
    project_orders = Project_Order.objects.all()
    # 渲染项目方案订单列表模板
    return render(request, 'core/project_order.html', {'project_orders': project_orders})


#方案详情视图函数
@login_required
def project_order_detail(request, pk):
    """项目方案详情视图函数"""
    # 获取指定ID的项目方案订单，不存在则返回404
    project_order = get_object_or_404(Project_Order, pk=pk)
    # 获取该方案关联的所有样品
    samples = project_order.samples.all()
    # 获取该方案关联的所有测试类型
    test_types = project_order.test_types.all()
    # 获取该方案关联的所有标准
    standards = project_order.standards.all()
    
    # 渲染项目方案详情模板
    return render(request, 'core/project_order_detail.html', {
        'project_order': project_order,
        'samples': samples,
        'test_types': test_types,
        'standards': standards
    })


# 添加报告相关视图函数
@login_required
def report_list(request):
    """报告列表视图函数"""
    # 获取所有报告
    reports = Report.objects.all()
    # 渲染报告列表模板
    return render(request, 'core/report.html', {'reports': reports})


@login_required
def report_detail(request, pk):
    """报告详情视图函数"""
    # 获取指定ID的报告，不存在则返回404
    report = get_object_or_404(Report, pk=pk)
    # 获取报告关联的方案
    project_order = report.project_order
    # 获取该方案关联的所有样品
    samples = project_order.samples.all() if project_order else []
    # 获取该报告关联的所有测试结果
    try:
        test_results = report.test_results.all()
    except AttributeError:
        test_results = []
    # 获取该方案关联的所有测试类型
    test_types = project_order.test_types.all() if project_order else []
    # 获取该方案关联的所有标准
    standards = project_order.standards.all() if project_order else []
    # 渲染报告详情模板
    return render(request, 'core/report_detail.html', {
        'report': report,
        'project_order': project_order,
        'samples': samples,
        'test_types': test_types,
        'standards': standards,
        'test_results': test_results
    })


def generate_pdf_report(request, pk):
    """生成PDF报告视图函数"""
    # 获取指定ID的报告，不存在则返回404
    report = get_object_or_404(Report, pk=pk)
    # 获取报告关联的方案
    project_order = report.project_order
    # 获取该方案关联的所有样品
    samples = project_order.samples.all() if project_order else []
    # 获取该报告关联的所有测试结果
    try:
        test_results = report.test_results.all()
    except AttributeError:
        test_results = []
    # 获取该方案关联的所有测试类型
    test_types = project_order.test_types.all() if project_order else []
    # 获取该方案关联的所有标准
    standards = project_order.standards.all() if project_order else []
    
    # 渲染HTML模板
    html_string = render_to_string('core/report_pdf.html', {
        'report': report,
        'project_order': project_order,
        'samples': samples,
        'test_types': test_types,
        'standards': standards,
        'test_results': test_results
    })
    
    # 生成PDF
    html = HTML(string=html_string)
    pdf = html.write_pdf()
    
    # 创建临时文件
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
        temp_file.write(pdf)
        temp_file_path = temp_file.name
    
    # 保存PDF文件到报告模型
    with open(temp_file_path, 'rb') as f:
        report.pdf_file.save(f'{report.report_id}.pdf', f)
    
    # 删除临时文件
    os.unlink(temp_file_path)
    
    # 显示成功消息
    messages.success(request, 'PDF报告生成成功！')
    return redirect('report_detail', pk=pk)


@login_required
def report_approve(request, pk):
    """报告审核视图函数"""
    # 获取指定ID的报告，不存在则返回404
    report = get_object_or_404(Report, pk=pk)
    
    # 检查用户权限（只有管理员或有权限的用户才能审核报告）
    if not request.user.is_superuser and not request.user.has_perm('core.can_approve_report'):
        messages.error(request, '您没有权限审核报告！')
        return redirect('report_detail', pk=pk)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'approve':
            # 审核通过，更新报告状态为报告审核中
            report.status = 'in_progress'
            messages.success(request, '报告已提交审核！')
        elif action == 'sign':
            # 签发报告，更新报告状态为报告签发
            report.status = 'completed'
            messages.success(request, '报告已签发！')
            # 生成PDF报告
            generate_pdf_report(request, pk)
        elif action == 'reject':
            # 拒绝报告，更新报告状态为报告编制
            report.status = 'pending'
            messages.error(request, '报告已拒绝，请重新编辑！')
        
        # 保存报告状态变更
        report.save()
        
    # 重定向回报告详情页
    return redirect('report_detail', pk=pk)


@login_required
def department_list(request):
    """部门列表视图函数"""
    # 获取所有部门
    departments = Department.objects.all()
    # 渲染部门列表模板
    return render(request, 'core/department.html', {'departments': departments})


# 删除功能视图函数
@login_required
def client_delete(request, pk):
    """删除客户视图函数"""
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        client.delete()
        messages.success(request, '客户已成功删除！')
    return redirect('client_list')

@login_required
def sample_delete(request, pk):
    """删除样品视图函数"""
    sample = get_object_or_404(Sample, pk=pk)
    if request.method == 'POST':
        sample.delete()
        messages.success(request, '样品已成功删除！')
    return redirect('sample_list')

@login_required
def order_delete(request, pk):
    """删除订单视图函数"""
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        messages.success(request, '订单已成功删除！')
    return redirect('order_list')

@login_required
def project_order_delete(request, pk):
    """删除项目方案视图函数"""
    project_order = get_object_or_404(Project_Order, pk=pk)
    if request.method == 'POST':
        project_order.delete()
        messages.success(request, '项目方案已成功删除！')
    return redirect('project_order_list')

@login_required
def report_delete(request, pk):
    """删除报告视图函数"""
    report = get_object_or_404(Report, pk=pk)
    if request.method == 'POST':
        report.delete()
        messages.success(request, '报告已成功删除！')
    return redirect('report_list')

@require_GET
def get_orders(request):
    """获取指定客户的订单"""
    client_id = request.GET.get('client_id')
    if not client_id:
        return JsonResponse({'orders': []})
    
    orders = Order.objects.filter(client_id=client_id)
    orders_list = [{'id': order.id, 'name': order.name, 'order_id': order.order_id} for order in orders]
    
    return JsonResponse({'orders': orders_list})


@login_required
def standard_list(request):
    """标准管理视图函数"""
    # 获取所有标准
    standards = Standard.objects.all()
    # 获取所有标准库
    libraries = StandardLibrary.objects.all()
    # 获取所有放射卫生标准
    radiation_hygiene = Standard_radiation_hygiene.objects.all()
    # 渲染标准管理模板
    return render(request, 'core/standard.html', {'standards': standards, 'libraries': libraries, 'radiation_hygiene': radiation_hygiene})
