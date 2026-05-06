# 导入Django快捷函数
from django.shortcuts import render, get_object_or_404, redirect
# 导入登录验证装饰器
from django.contrib.auth.decorators import login_required
# 导入权限装饰器
from .decorators import require_permission
# 导入请求方法装饰器
from django.views.decorators.http import require_GET
# 导入JSON响应模块
from django.http import JsonResponse, HttpResponse
# 导入模型
from .models import Client, Sample, Test, Order, Staff, Project_Order, Report, Department, SampleType, SampleTypeDescription, Position
# 导入standard应用的模型
from standard.models import Standard, StandardLibrary, Standard_radiation_hygiene

# 导入消息框架
from django.contrib import messages
# 导入ORM聚合函数和Q对象
from django.db.models import Count, Q
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
from django.contrib.auth import authenticate, login


def user_login(request):
    """自定义登录视图函数"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # 尝试认证
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_active:
                # 登录成功
                login(request, user)
                messages.success(request, f'登录成功！欢迎回来，{user.username}')
                return redirect('home')
            else:
                messages.error(request, '账号已被禁用')
        else:
            messages.error(request, '用户名或密码错误')
    
    # GET请求或登录失败，显示登录页面
    return render(request, 'core/login.html')


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
    
    # 统计不同样品类型的样品数量（用于饼图）
    sample_type_data = Sample.objects.values('sample_type__name').annotate(count=Count('sample_type'))
    # 准备样品类型饼图数据：标签（样品类型名称）和值（数量）
    sample_labels = [item['sample_type__name'] or '未分类' for item in sample_type_data]
    sample_values = [item['count'] for item in sample_type_data]
    # 将样品类型数据转换为JSON格式（便于前端JavaScript使用）
    sample_chart_data = {
        'labels': sample_labels,
        'values': sample_values
    }
    
    # 统计不同客户的订单数量（用于饼图）
    order_client_data = Order.objects.values('client__name').annotate(count=Count('client'))
    # 准备订单客户饼图数据：标签（客户名称）和值（数量）
    order_labels = [item['client__name'] or '未知客户' for item in order_client_data]
    order_values = [item['count'] for item in order_client_data]
    # 将订单客户数据转换为JSON格式（便于前端JavaScript使用）
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
    
    # 统计不同状态的测试数量（用于饼图）
    test_status_data = Test.objects.values('status').annotate(count=Count('status'))
    # 准备测试状态饼图数据：标签（状态）和值（数量）
    test_labels = [item['status'] for item in test_status_data]
    test_values = [item['count'] for item in test_status_data]
    # 将测试状态数据转换为JSON格式（便于前端JavaScript使用）
    test_chart_data = {
        'labels': test_labels,
        'values': test_values
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
        'report_chart_data': json.dumps(report_chart_data),   # 添加报告状态饼图数据
        'test_chart_data': json.dumps(test_chart_data)        # 添加测试状态饼图数据
    }
    
    # 渲染首页模板
    return render(request, 'core/home.html', context)


@login_required
@require_permission('can_manage_clients')
def client_list(request):
    """客户列表视图函数"""
    # 获取搜索关键词
    search_query = request.GET.get('search', '')
    
    # 获取所有客户
    clients = Client.objects.all()
    
    # 如果有搜索关键词，进行筛选
    if search_query:
        clients = clients.filter(
            Q(name__icontains=search_query) |
            Q(province__icontains=search_query) |
            Q(city__icontains=search_query)
        )
    
    # 渲染客户列表模板
    return render(request, 'core/client_list.html', {
        'clients': clients,
        'search_query': search_query
    })


@login_required
def client_create(request):
    """添加客户视图函数"""
    if request.method == 'POST':
        # 获取表单数据
        name = request.POST['name']
        contact_person = request.POST['contact_person']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        province = request.POST.get('province', '')
        city = request.POST.get('city', '')
        
        # 创建客户对象
        client = Client(
            name=name,
            contact_person=contact_person,
            email=email,
            phone=phone,
            address=address,
            province=province,
            city=city
        )
        client.save()
        
        # 显示成功消息
        messages.success(request, '客户添加成功！')
        # 重定向到客户列表页面
        return redirect('client_list')
    
    # 渲染添加客户模板
    return render(request, 'core/client_create.html')


@login_required
def client_edit(request, pk):
    """编辑客户视图函数"""
    # 获取指定ID的客户，不存在则返回404
    client = get_object_or_404(Client, pk=pk)
    
    if request.method == 'POST':
        # 获取表单数据
        name = request.POST['name']
        contact_person = request.POST['contact_person']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        province = request.POST.get('province', '')
        city = request.POST.get('city', '')
        
        # 更新客户对象
        client.name = name
        client.contact_person = contact_person
        client.email = email
        client.phone = phone
        client.address = address
        client.province = province
        client.city = city
        client.save()
        
        # 显示成功消息
        messages.success(request, '客户更新成功！')
        # 重定向到客户列表页面
        return redirect('client_list')
    
    # 渲染编辑客户模板
    return render(request, 'core/client_edit.html', {'client': client})


@login_required
@require_permission('can_manage_samples')
def sample_list(request):
    """样品列表视图函数"""
    # 获取搜索关键词
    search_query = request.GET.get('search', '')
    
    # 获取所有样品，支持搜索
    samples = Sample.objects.all()
    
    if search_query:
        # 支持按样品ID、客户名称、方案ID、方案名称、订单ID、订单名称、样品类型搜索
        samples = samples.filter(
            Q(sample_id__icontains=search_query) |
            Q(client__name__icontains=search_query) |
            Q(project_order__project_id__icontains=search_query) |
            Q(project_order__name__icontains=search_query) |
            Q(order__order_id__icontains=search_query) |
            Q(order__name__icontains=search_query) |
            Q(sample_type__name__icontains=search_query) |
            Q(sample_type_description__description__icontains=search_query)
        )
    
    # 渲染样品列表模板
    return render(request, 'core/sample_list.html', {'samples': samples, 'search_query': search_query})


@login_required
def sample_create(request):
    """添加样品视图函数"""
    # 获取所有客户
    clients = Client.objects.all()
    # 获取所有订单
    orders = Order.objects.all()
    # 获取所有样品类型
    sample_types = SampleType.objects.all()
    
    if request.method == 'POST':
        # 获取表单数据
        client_id = request.POST['client']
        order_id = request.POST.get('order')
        sample_type_id = request.POST.get('sample_type')
        collection_date = request.POST['collection_date']
        
        # 获取客户对象
        client = Client.objects.get(pk=client_id)
        
        # 获取订单对象（可为空）
        order = None
        if order_id:
            order = Order.objects.get(pk=order_id)
        
        # 获取样品类型对象（可为空）
        sample_type = None
        if sample_type_id:
            sample_type = SampleType.objects.get(pk=sample_type_id)
        
        # 创建样品对象
        sample = Sample(
            client=client,
            order=order,
            sample_type=sample_type,
            collection_date=collection_date,
            status='pending',
            created_by=request.user
        )
        sample.save()
        
        # 显示成功消息
        messages.success(request, '样品添加成功！')
        # 重定向到样品列表页面
        return redirect('sample_list')
    
    # 渲染添加样品模板
    return render(request, 'core/sample_create.html', {
        'clients': clients,
        'orders': orders,
        'sample_types': sample_types
    })


@login_required
def sample_edit(request, pk):
    """编辑样品视图函数"""
    # 获取指定ID的样品，不存在则返回404
    sample = get_object_or_404(Sample, pk=pk)
    # 获取所有客户
    clients = Client.objects.all()
    # 获取所有订单
    orders = Order.objects.all()
    # 获取所有样品类型
    sample_types = SampleType.objects.all()
    
    if request.method == 'POST':
        # 获取表单数据
        client_id = request.POST['client']
        order_id = request.POST.get('order')
        sample_type_id = request.POST.get('sample_type')
        collection_date = request.POST['collection_date']
        
        # 获取客户对象
        client = Client.objects.get(pk=client_id)
        
        # 获取订单对象（可为空）
        order = None
        if order_id:
            order = Order.objects.get(pk=order_id)
        
        # 获取样品类型对象（可为空）
        sample_type = None
        if sample_type_id:
            sample_type = SampleType.objects.get(pk=sample_type_id)
        
        # 更新样品对象
        sample.client = client
        sample.order = order
        sample.sample_type = sample_type
        sample.collection_date = collection_date
        sample.save()
        
        # 显示成功消息
        messages.success(request, '样品更新成功！')
        # 重定向到样品列表页面
        return redirect('sample_list')
    
    # 渲染编辑样品模板
    return render(request, 'core/sample_edit.html', {
        'sample': sample,
        'clients': clients,
        'orders': orders,
        'sample_types': sample_types
    })


@login_required
@require_permission('can_manage_tests')
def test_list(request):
    """测试列表视图函数"""
    # 获取所有样品
    samples = Sample.objects.all()
    
    # 为每个没有测试的样品自动创建测试
    for sample in samples:
        # 检查该样品是否已有测试
        existing_tests = Test.objects.filter(sample=sample)
        if not existing_tests.exists():
            # 获取样品关联的方案
            if sample.project_order:
                # 获取方案关联的测试类型
                test_types = sample.project_order.test_types.all()
                # 为每个测试类型创建测试
                for test_type in test_types:
                    Test.objects.create(
                        sample=sample,
                        test_type=test_type,
                        status='pending',
                        address='',
                        field_data=''
                    )
    
    # 获取搜索关键词
    search_query = request.GET.get('search', '')
    
    # 获取所有测试
    tests = Test.objects.all()
    
    # 如果有搜索关键词，进行模糊搜索
    if search_query:
        from django.db.models import Q
        tests = tests.filter(
            Q(sample__sample_id__icontains=search_query) |
            Q(sample__sample_type__name__icontains=search_query) |
            Q(sample__sample_type_description__description__icontains=search_query) |
            Q(status__icontains=search_query) |
            Q(result__icontains=search_query) |
            Q(address__icontains=search_query) |
            Q(analyzed_by__username__icontains=search_query) |
            Q(verified_by__username__icontains=search_query)
        )
    
    # 渲染测试列表模板
    return render(request, 'core/test_list.html', {'tests': tests, 'search_query': search_query})


@login_required
def test_create(request):
    """添加测试视图函数"""
    # 获取所有样品
    samples = Sample.objects.all()
    # 获取所有用户（用于分析人员和验证人员选择）
    users = User.objects.all()
    
    if request.method == 'POST':
        # 获取表单数据
        sample_id = request.POST['sample']
        status = request.POST['status']
        result = request.POST.get('result', '')
        analyzed_by_id = request.POST.get('analyzed_by')
        verified_by_id = request.POST.get('verified_by')
        analysis_date = request.POST.get('analysis_date')
        verification_date = request.POST.get('verification_date')
        
        # 获取样品对象
        sample = Sample.objects.get(pk=sample_id)
        # 获取样品关联的测试类型（如果有）
        test_type = None
        
        # 获取分析人员对象（可为空）
        analyzed_by = None
        if analyzed_by_id:
            analyzed_by = User.objects.get(pk=analyzed_by_id)
        
        # 获取验证人员对象（可为空）
        verified_by = None
        if verified_by_id:
            verified_by = User.objects.get(pk=verified_by_id)
        
        # 创建测试对象
        test = Test(
            sample=sample,
            test_type=test_type,
            status=status,
            result=result,
            analyzed_by=analyzed_by,
            verified_by=verified_by,
            analysis_date=analysis_date if analysis_date else None,
            verification_date=verification_date if verification_date else None,
            address=request.POST.get('address', '')
        )
        test.save()
        
        # 处理照片上传
        if 'photo' in request.FILES:
            test.photo = request.FILES['photo']
            test.save()
        
        # 显示成功消息
        messages.success(request, '测试添加成功！')
        # 重定向到测试列表页面
        return redirect('test_list')
    
    # 渲染添加测试模板
    return render(request, 'core/test_create.html', {
        'samples': samples,
        'users': users
    })


@login_required
def test_edit(request, pk):
    """编辑测试视图函数"""
    # 获取指定ID的测试，不存在则返回404
    test = get_object_or_404(Test, pk=pk)
    # 获取所有样品
    samples = Sample.objects.all()
    # 获取所有用户（用于分析人员和验证人员选择）
    users = User.objects.all()
    
    if request.method == 'POST':
        # 获取表单数据
        sample_id = request.POST['sample']
        status = request.POST['status']
        result = request.POST.get('result', '')
        analyzed_by_id = request.POST.get('analyzed_by')
        verified_by_id = request.POST.get('verified_by')
        analysis_date = request.POST.get('analysis_date')
        verification_date = request.POST.get('verification_date')
        
        # 获取样品对象
        sample = Sample.objects.get(pk=sample_id)
        # 获取样品关联的测试类型（如果有）
        test_type = None
        
        # 获取分析人员对象（可为空）
        analyzed_by = None
        if analyzed_by_id:
            analyzed_by = User.objects.get(pk=analyzed_by_id)
        
        # 获取验证人员对象（可为空）
        verified_by = None
        if verified_by_id:
            verified_by = User.objects.get(pk=verified_by_id)
        
        # 更新测试对象
        test.sample = sample
        test.test_type = test_type
        test.status = status
        test.result = result
        test.analyzed_by = analyzed_by
        test.verified_by = verified_by
        test.analysis_date = analysis_date if analysis_date else None
        test.verification_date = verification_date if verification_date else None
        test.address = request.POST.get('address', '')
        test.save()
        
        # 处理照片上传
        if 'photo' in request.FILES:
            test.photo = request.FILES['photo']
            test.save()
        
        # 更新关联的报告信息
        if sample.project_order:
            try:
                report = Report.objects.get(project_order=sample.project_order)
                # 更新报告的样品关联
                report.samples.clear()
                report.samples.add(*sample.project_order.samples.all())
                
                # 更新报告的测试结果关联
                report.test_results.clear()
                report.test_results.add(*Test.objects.filter(sample__project_order=sample.project_order))
                
                # 更新报告的测试类型关联
                report.test_types.clear()
                report.test_types.add(*sample.project_order.test_types.all())
                
                report.save()
            except Report.DoesNotExist:
                pass
        
        # 显示成功消息
        messages.success(request, '测试更新成功！报告已同步更新。')
        # 重定向到测试列表页面
        return redirect('test_list')
    
    # 渲染编辑测试模板
    return render(request, 'core/test_edit.html', {
        'test': test,
        'samples': samples,
        'users': users
    })

@login_required
@require_permission('can_manage_orders')
def order_list(request):
    """订单列表视图函数"""
    # 获取所有订单
    orders = Order.objects.all()
    # 渲染订单列表模板
    return render(request, 'core/order_list.html', {'orders': orders})


@login_required
def order_create(request):
    """添加订单视图函数"""
    # 获取所有客户
    clients = Client.objects.all()
    
    if request.method == 'POST':
        # 获取表单数据
        name = request.POST['name']
        description = request.POST['description']
        client_id = request.POST['client']
        status = request.POST['status']
        
        # 获取客户对象
        client = Client.objects.get(pk=client_id)
        
        # 创建订单对象
        order = Order(
            name=name,
            description=description,
            client=client,
            status=status,
            created_by=request.user
        )
        order.save()
        
        # 显示成功消息
        messages.success(request, '订单添加成功！')
        # 重定向到订单列表页面
        return redirect('order_list')
    
    # 渲染添加订单模板
    return render(request, 'core/order_create.html', {'clients': clients})


@login_required
def order_edit(request, pk):
    """编辑订单视图函数"""
    # 获取指定ID的订单，不存在则返回404
    order = get_object_or_404(Order, pk=pk)
    # 获取所有客户
    clients = Client.objects.all()
    
    if request.method == 'POST':
        # 获取表单数据
        name = request.POST['name']
        description = request.POST['description']
        client_id = request.POST['client']
        status = request.POST['status']
        
        # 获取客户对象
        client = Client.objects.get(pk=client_id)
        
        # 更新订单对象
        order.name = name
        order.description = description
        order.client = client
        order.status = status
        order.save()
        
        # 显示成功消息
        messages.success(request, '订单更新成功！')
        # 重定向到订单列表页面
        return redirect('order_list')
    
    # 渲染编辑订单模板
    return render(request, 'core/order_edit.html', {'order': order, 'clients': clients})
    



# 组织架构管理视图函数
@login_required
@require_permission('can_manage_org')
def org_manage(request):
    """组织架构管理视图 (部门和职务)"""
    departments = Department.objects.all()
    positions = Position.objects.all()
    return render(request, 'core/org_manage.html', {
        'departments': departments,
        'positions': positions
    })

@login_required
def department_create(request):
    """创建部门"""
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        Department.objects.create(
            name=name,
            description=description,
            created_by=request.user
        )
        messages.success(request, '部门创建成功！')
        return redirect('org_manage')
    return render(request, 'core/department_form.html')

@login_required
def department_edit(request, pk):
    """编辑部门"""
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        department.name = request.POST.get('name')
        department.description = request.POST.get('description')
        department.save()
        messages.success(request, '部门信息已更新！')
        return redirect('org_manage')
    return render(request, 'core/department_form.html', {'department': department})

@login_required
def department_delete(request, pk):
    """删除部门"""
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        # 检查是否有员工关联此部门
        if Staff.objects.filter(department=department).exists():
            messages.error(request, '无法删除该部门，因为仍有员工隶属于此。')
            return redirect('org_manage')
        department.delete()
        messages.success(request, '部门已删除！')
        return redirect('org_manage')
    return render(request, 'core/department_confirm_delete.html', {'department': department})

@login_required
def position_create(request):
    """创建职务"""
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        Position.objects.create(
            name=name,
            description=description,
            created_by=request.user
        )
        messages.success(request, '职务创建成功！')
        return redirect('org_manage')
    return render(request, 'core/position_form.html')

@login_required
def position_edit(request, pk):
    """编辑职务"""
    position = get_object_or_404(Position, pk=pk)
    if request.method == 'POST':
        position.name = request.POST.get('name')
        position.description = request.POST.get('description')
        position.save()
        messages.success(request, '职务信息已更新！')
        return redirect('org_manage')
    return render(request, 'core/position_form.html', {'position': position})

@login_required
def position_delete(request, pk):
    """删除职务"""
    position = get_object_or_404(Position, pk=pk)
    if request.method == 'POST':
        # 检查是否有员工关联此职务
        if Staff.objects.filter(position_link=position).exists():
            messages.error(request, '无法删除该职务，因为仍有员工担任此职。')
            return redirect('org_manage')
        position.delete()
        messages.success(request, '职务已删除！')
        return redirect('org_manage')
    return render(request, 'core/position_confirm_delete.html', {'position': position})

@login_required
@require_permission('can_manage_staff')
def staff_list(request):
    """员工列表视图函数"""
    # 获取所有员工
    staffs = Staff.objects.all()
    # 渲染员工列表模板
    return render(request, 'core/staff.html', {'staffs': staffs})


@login_required
def staff_create(request):
    """添加员工视图函数"""
    # 获取所有部门
    departments = Department.objects.all()
    # 获取所有职务
    positions = Position.objects.all()
    
    if request.method == 'POST':
        # 获取表单数据
        name = request.POST['name']
        department_id = request.POST['department']
        position_id = request.POST['position']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        
        # 获取部门对象
        department = Department.objects.get(pk=department_id)
        # 获取职务对象
        position = Position.objects.get(pk=position_id) if position_id else None
        
        # 创建员工对象
        staff = Staff(
            name=name,
            department=department,
            position_link=position,
            email=email,
            phone=phone,
            address=address,
            created_by=request.user,
            # 权限设置
            is_active=request.POST.get('is_active') == 'on',
            can_manage_clients=request.POST.get('can_manage_clients') == 'on',
            can_manage_orders=request.POST.get('can_manage_orders') == 'on',
            can_manage_projects=request.POST.get('can_manage_projects') == 'on',
            can_manage_samples=request.POST.get('can_manage_samples') == 'on',
            can_manage_tests=request.POST.get('can_manage_tests') == 'on',
            can_manage_reports=request.POST.get('can_manage_reports') == 'on',
            can_manage_standard=request.POST.get('can_manage_standard') == 'on',
            can_manage_staff=request.POST.get('can_manage_staff') == 'on',
            can_manage_org=request.POST.get('can_manage_org') == 'on',
            can_manage_sample_types=request.POST.get('can_manage_sample_types') == 'on',
            can_manage_sample_descriptions=request.POST.get('can_manage_sample_descriptions') == 'on',
            can_access_admin=request.POST.get('can_access_admin') == 'on'
        )
        staff.save()
        
        # 如果启用登录，创建用户账号
        if staff.is_active and email:
            # 生成默认密码（员工编号）
            password = staff.staff_id or '123456'
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password
            )
            staff.user = user
            staff.save()
        
        # 显示成功消息
        messages.success(request, '员工添加成功！')
        # 重定向到员工列表页面
        return redirect('staff_list')
    
    # 渲染添加员工模板
    return render(request, 'core/staff_create.html', {
        'departments': departments,
        'positions': positions
    })


@login_required
def staff_edit(request, pk):
    """编辑员工视图函数"""
    # 获取指定ID的员工，不存在则返回404
    staff = get_object_or_404(Staff, pk=pk)
    # 获取所有部门
    departments = Department.objects.all()
    # 获取所有职务
    positions = Position.objects.all()
    
    if request.method == 'POST':
        # 获取表单数据
        name = request.POST['name']
        department_id = request.POST['department']
        position_id = request.POST['position']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        
        # 获取部门对象
        department = Department.objects.get(pk=department_id)
        # 获取职务对象
        position = Position.objects.get(pk=position_id) if position_id else None
        
        # 更新员工对象
        staff.name = name
        staff.department = department
        staff.position_link = position
        staff.email = email
        staff.phone = phone
        staff.address = address
        
        # 更新权限设置
        staff.is_active = request.POST.get('is_active') == 'on'
        staff.can_manage_clients = request.POST.get('can_manage_clients') == 'on'
        staff.can_manage_orders = request.POST.get('can_manage_orders') == 'on'
        staff.can_manage_projects = request.POST.get('can_manage_projects') == 'on'
        staff.can_manage_samples = request.POST.get('can_manage_samples') == 'on'
        staff.can_manage_tests = request.POST.get('can_manage_tests') == 'on'
        staff.can_manage_reports = request.POST.get('can_manage_reports') == 'on'
        staff.can_manage_standard = request.POST.get('can_manage_standard') == 'on'
        staff.can_manage_staff = request.POST.get('can_manage_staff') == 'on'
        staff.can_manage_org = request.POST.get('can_manage_org') == 'on'
        staff.can_manage_sample_types = request.POST.get('can_manage_sample_types') == 'on'
        staff.can_manage_sample_descriptions = request.POST.get('can_manage_sample_descriptions') == 'on'
        staff.can_access_admin = request.POST.get('can_access_admin') == 'on'
        
        staff.save()
        
        # 如果启用登录且没有关联用户，创建用户账号
        if staff.is_active and email and not staff.user:
            password = staff.staff_id or '123456'
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password
            )
            staff.user = user
            staff.save()
        
        # 如果禁用登录，禁用关联用户
        if not staff.is_active and staff.user:
            staff.user.is_active = False
            staff.user.save()
        
        # 显示成功消息
        messages.success(request, '员工更新成功！')
        # 重定向到员工列表页面
        return redirect('staff_list')
    
    # 渲染编辑员工模板
    return render(request, 'core/staff_edit.html', {
        'staff': staff, 
        'departments': departments,
        'positions': positions
    })


@login_required
def staff_delete(request, pk):
    """删除员工视图函数"""
    # 获取指定ID的员工，不存在则返回404
    staff = get_object_or_404(Staff, pk=pk)
    
    if request.method == 'POST':
        # 执行删除操作
        staff.delete()
        # 显示成功消息
        messages.success(request, '员工已成功删除！')
        # 重定向到员工列表页面
        return redirect('staff_list')
    
    # GET请求时，渲染删除确认页面
    return render(request, 'core/staff_confirm_delete.html', {'staff': staff})

#方案订单列表视图函数
@login_required
@require_permission('can_manage_projects')
def project_order_list(request):
    """项目方案订单列表视图函数"""
    # 获取所有项目方案订单
    project_orders = Project_Order.objects.all()
    # 渲染项目方案订单列表模板
    return render(request, 'core/project_order.html', {'project_orders': project_orders})


@login_required
def get_client_orders(request):
    """获取客户相关订单的API接口"""
    client_id = request.GET.get('client_id')
    if not client_id:
        return JsonResponse({'orders': []})
    
    try:
        # 获取该客户的所有订单
        orders = Order.objects.filter(client_id=client_id)
        orders_data = [{'id': order.id, 'name': order.name, 'order_id': order.order_id} for order in orders]
        return JsonResponse({'orders': orders_data})
    except Exception as e:
        return JsonResponse({'orders': [], 'error': str(e)})


@login_required
def project_order_create(request):
    """添加方案视图函数"""
    # 获取所有客户
    clients = Client.objects.all()
    # 获取所有订单
    orders = Order.objects.all()
    # 获取所有员工
    staffs = Staff.objects.all()
    # 获取所有样品类型
    sample_types = SampleType.objects.all()
    # 获取所有样品类型描述
    sample_type_descriptions = SampleTypeDescription.objects.all()
    # 获取所有测试类型（Standard模型）
    test_types = Standard.objects.all()
    # 获取所有标准（Standard_radiation_hygiene模型）
    standards = Standard_radiation_hygiene.objects.all()
    
    if request.method == 'POST':
        # 获取表单数据
        name = request.POST['name']
        description = request.POST['description']
        client_id = request.POST['client']
        order_id = request.POST['order']
        status = request.POST['status']
        
        # 获取客户和订单对象
        client = Client.objects.get(pk=client_id)
        order = Order.objects.get(pk=order_id)
        
        # 创建方案对象
        project_order = Project_Order(
            name=name,
            description=description,
            client=client,
            order=order,
            status=status,
            created_by=request.user
        )
        project_order.save()
        
        # 处理多对多关系
        # 添加员工
        staff_ids = request.POST.getlist('staff')
        for staff_id in staff_ids:
            project_order.staff.add(staff_id)
        
        # 添加样品类型（支持多选）
        sample_type_ids = request.POST.getlist('sample_types')
        for sample_type_id in sample_type_ids:
            project_order.sample_types.add(sample_type_id)
        
        # 添加样品类型描述（支持多选，格式为 desc_id:quantity）
        sample_type_description_data = request.POST.getlist('sample_type_descriptions')
        quantities = {}
        for desc_data in sample_type_description_data:
            # 解析格式 desc_id:quantity
            parts = desc_data.split(':')
            desc_id = parts[0]
            quantity = int(parts[1]) if len(parts) > 1 else 1
            project_order.sample_type_descriptions.add(desc_id)
            quantities[desc_id] = quantity
        
        # 保存数量信息
        project_order.sample_type_description_quantities = quantities
        project_order.save()  # 再次保存以保存数量信息
        
        # 根据样品描述和数量自动创建样品
        from datetime import datetime
        for desc_id, quantity in quantities.items():
            try:
                sample_type_description = SampleTypeDescription.objects.get(pk=desc_id)
                for i in range(quantity):
                    Sample.objects.create(
                        client=client,
                        order=order,
                        project_order=project_order,
                        sample_type=sample_type_description.sample_type,
                        sample_type_description=sample_type_description,
                        collection_date=datetime.now()
                    )
            except SampleTypeDescription.DoesNotExist:
                pass
        
        # 添加测试类型
        test_type_ids = request.POST.getlist('test_types')
        for test_type_id in test_type_ids:
            project_order.test_types.add(test_type_id)
        
        # 添加标准
        standard_ids = request.POST.getlist('standards')
        for standard_id in standard_ids:
            project_order.standards.add(standard_id)
        
        # 自动创建报告
        report = Report.objects.create(
            project_order=project_order,
            name=f'{project_order.name} - 报告',
            description=f'自动生成的报告，关联方案: {project_order.name}',
            client=client,
            order=order,
            created_by=request.user
        )
        
        # 显示成功消息
        messages.success(request, '方案添加成功！样品和报告已自动创建。')
        # 重定向到方案列表页面
        return redirect('project_order_list')
    
    # 渲染添加方案模板
    return render(request, 'core/project_order_create.html', {
        'clients': clients,
        'orders': orders,
        'staffs': staffs,
        'sample_types': sample_types,
        'sample_type_descriptions': sample_type_descriptions,
        'test_types': test_types,
        'standards': standards
    })


@login_required
def project_order_edit(request, pk):
    """编辑方案视图函数"""
    # 获取指定ID的方案，不存在则返回404
    project_order = get_object_or_404(Project_Order, pk=pk)
    # 获取所有客户
    clients = Client.objects.all()
    # 获取所有订单
    orders = Order.objects.all()
    # 获取所有员工
    staffs = Staff.objects.all()
    # 获取所有样品类型
    sample_types = SampleType.objects.all()
    # 获取所有样品类型描述
    sample_type_descriptions = SampleTypeDescription.objects.all()
    # 获取所有测试类型（Standard模型）
    test_types = Standard.objects.all()
    # 获取所有标准（Standard_radiation_hygiene模型）
    standards = Standard_radiation_hygiene.objects.all()
    
    if request.method == 'POST':
        # 获取表单数据
        name = request.POST['name']
        description = request.POST['description']
        client_id = request.POST['client']
        order_id = request.POST['order']
        status = request.POST['status']
        
        # 获取客户和订单对象
        client = Client.objects.get(pk=client_id)
        order = Order.objects.get(pk=order_id)
        
        # 更新方案对象
        project_order.name = name
        project_order.description = description
        project_order.client = client
        project_order.order = order
        project_order.status = status
        project_order.save()
        
        # 处理多对多关系
        # 更新员工
        staff_ids = request.POST.getlist('staff')
        project_order.staff.clear()
        for staff_id in staff_ids:
            project_order.staff.add(staff_id)
        
        # 更新样品类型（支持多选）
        sample_type_ids = request.POST.getlist('sample_types')
        project_order.sample_types.clear()
        for sample_type_id in sample_type_ids:
            project_order.sample_types.add(sample_type_id)
        
        # 更新样品类型描述（支持多选，格式为 desc_id:quantity）
        sample_type_description_data = request.POST.getlist('sample_type_descriptions')
        project_order.sample_type_descriptions.clear()
        quantities = {}
        for desc_data in sample_type_description_data:
            # 解析格式 desc_id:quantity
            parts = desc_data.split(':')
            desc_id = parts[0]
            quantity = int(parts[1]) if len(parts) > 1 else 1
            project_order.sample_type_descriptions.add(desc_id)
            quantities[desc_id] = quantity
        
        # 保存数量信息
        project_order.sample_type_description_quantities = quantities
        project_order.save()  # 再次保存以保存数量信息
        
        # 根据新的样品描述和数量更新样品（先删除旧样品，再创建新样品）
        from datetime import datetime
        # 删除该方案的所有旧样品
        Sample.objects.filter(project_order=project_order).delete()
        # 创建新样品
        for desc_id, quantity in quantities.items():
            try:
                sample_type_description = SampleTypeDescription.objects.get(pk=desc_id)
                for i in range(quantity):
                    Sample.objects.create(
                        client=client,
                        order=order,
                        project_order=project_order,
                        sample_type=sample_type_description.sample_type,
                        sample_type_description=sample_type_description,
                        collection_date=datetime.now()
                    )
            except SampleTypeDescription.DoesNotExist:
                pass
        
        # 更新测试类型
        test_type_ids = request.POST.getlist('test_types')
        project_order.test_types.clear()
        for test_type_id in test_type_ids:
            project_order.test_types.add(test_type_id)
        
        # 更新标准
        standard_ids = request.POST.getlist('standards')
        project_order.standards.clear()
        for standard_id in standard_ids:
            project_order.standards.add(standard_id)
        
        # 更新关联的报告（如果存在）
        try:
            report = Report.objects.get(project_order=project_order)
            report.name = f'{project_order.name} - 报告'
            report.description = f'自动生成的报告，关联方案: {project_order.name}'
            report.client = client
            report.order = order
            report.save()
        except Report.DoesNotExist:
            # 如果报告不存在，则创建一个新报告
            Report.objects.create(
                project_order=project_order,
                name=f'{project_order.name} - 报告',
                description=f'自动生成的报告，关联方案: {project_order.name}',
                client=client,
                order=order,
                created_by=request.user
            )
        
        # 显示成功消息
        messages.success(request, '方案更新成功！样品和报告已自动更新。')
        # 重定向到方案列表页面
        return redirect('project_order_list')
    
    # 获取样品描述数量信息
    sample_type_description_quantities = project_order.sample_type_description_quantities or {}
    
    # 渲染编辑方案模板
    return render(request, 'core/project_order_edit.html', {
        'project_order': project_order,
        'clients': clients,
        'orders': orders,
        'staffs': staffs,
        'sample_types': sample_types,
        'sample_type_descriptions': sample_type_descriptions,
        'sample_type_description_quantities': sample_type_description_quantities,
        'test_types': test_types,
        'standards': standards
    })


#方案详情视图函数
@login_required
def project_order_detail(request, pk):
    """项目方案详情视图函数"""
    # 获取指定ID的项目方案订单，不存在则返回404
    project_order = get_object_or_404(Project_Order, pk=pk)
    # 获取该方案关联的所有样品类型
    sample_types = project_order.sample_types.all()
    # 获取该方案关联的所有样品类型描述
    sample_type_descriptions = project_order.sample_type_descriptions.all()
    # 获取该方案关联的所有测试类型
    test_types = project_order.test_types.all()
    # 获取该方案关联的所有标准
    standards = project_order.standards.all()
    
    # 获取样品描述数量信息
    sample_type_description_quantities = project_order.sample_type_description_quantities or {}
    
    # 渲染项目方案详情模板
    return render(request, 'core/project_order_detail.html', {
        'project_order': project_order,
        'sample_types': sample_types,
        'sample_type_descriptions': sample_type_descriptions,
        'sample_type_description_quantities': sample_type_description_quantities,
        'test_types': test_types,
        'standards': standards
    })


# 添加报告相关视图函数
@login_required
@require_permission('can_manage_reports')
def report_list(request):
    """报告列表视图函数"""
    # 获取所有报告
    reports = Report.objects.all()
    # 渲染报告列表模板
    return render(request, 'core/report.html', {'reports': reports})


@login_required
def report_create(request):
    """添加报告视图函数"""
    # 获取所有方案
    project_orders = Project_Order.objects.all()
    # 获取所有客户
    clients = Client.objects.all()
    # 获取所有订单
    orders = Order.objects.all()
    # 获取所有员工
    staffs = Staff.objects.all()
    # 获取所有样品
    samples = Sample.objects.all()
    # 获取所有标准（测试类型）
    standards = Standard.objects.all()
    # 获取所有标准（标准）
    standard_radiation_hygiene = Standard_radiation_hygiene.objects.all()
    # 获取所有测试结果
    test_results = Test.objects.all()
    
    if request.method == 'POST':
        # 获取表单数据
        project_order_id = request.POST.get('project_order')
        name = request.POST['name']
        description = request.POST.get('description', '')
        client_id = request.POST['client']
        order_id = request.POST['order']
        status = request.POST['status']
        
        # 获取关联对象
        project_order = None
        if project_order_id:
            project_order = Project_Order.objects.get(pk=project_order_id)
        
        client = Client.objects.get(pk=client_id)
        order = Order.objects.get(pk=order_id)
        
        # 创建报告对象
        report = Report(
            project_order=project_order,
            name=name,
            description=description,
            client=client,
            order=order,
            status=status,
            created_by=request.user
        )
        report.save()
        
        # 处理多对多关系
        staff_ids = request.POST.getlist('staff')
        if staff_ids:
            report.staff.set(staff_ids)
        
        sample_ids = request.POST.getlist('samples')
        if sample_ids:
            report.samples.set(sample_ids)
        
        test_type_ids = request.POST.getlist('test_types')
        if test_type_ids:
            report.test_types.set(test_type_ids)
        
        standard_ids = request.POST.getlist('standards')
        if standard_ids:
            report.standards.set(standard_ids)
        
        test_result_ids = request.POST.getlist('test_results')
        if test_result_ids:
            report.test_results.set(test_result_ids)
        
        # 显示成功消息
        messages.success(request, '报告添加成功！')
        # 重定向到报告列表页面
        return redirect('report_list')
    
    # 渲染添加报告模板
    return render(request, 'core/report_create.html', {
        'project_orders': project_orders,
        'clients': clients,
        'orders': orders,
        'staffs': staffs,
        'samples': samples,
        'standards': standards,
        'standard_radiation_hygiene': standard_radiation_hygiene,
        'test_results': test_results
    })


@login_required
def report_edit(request, pk):
    """编辑报告视图函数"""
    # 获取指定ID的报告，不存在则返回404
    report = get_object_or_404(Report, pk=pk)
    # 获取所有方案
    project_orders = Project_Order.objects.all()
    # 获取所有客户
    clients = Client.objects.all()
    # 获取所有订单
    orders = Order.objects.all()
    # 获取所有员工
    staffs = Staff.objects.all()
    # 获取所有样品
    samples = Sample.objects.all()
    # 获取所有标准（测试类型）
    standards = Standard.objects.all()
    # 获取所有标准（标准）
    standard_radiation_hygiene = Standard_radiation_hygiene.objects.all()
    # 获取所有测试结果
    test_results = Test.objects.all()
    
    if request.method == 'POST':
        # 获取表单数据
        project_order_id = request.POST.get('project_order')
        name = request.POST['name']
        description = request.POST.get('description', '')
        client_id = request.POST['client']
        order_id = request.POST['order']
        status = request.POST['status']
        
        # 获取关联对象
        project_order = None
        if project_order_id:
            project_order = Project_Order.objects.get(pk=project_order_id)
        
        client = Client.objects.get(pk=client_id)
        order = Order.objects.get(pk=order_id)
        
        # 更新报告对象
        report.project_order = project_order
        report.name = name
        report.description = description
        report.client = client
        report.order = order
        report.status = status
        report.save()
        
        # 处理多对多关系
        staff_ids = request.POST.getlist('staff')
        report.staff.set(staff_ids)
        
        sample_ids = request.POST.getlist('samples')
        report.samples.set(sample_ids)
        
        test_type_ids = request.POST.getlist('test_types')
        report.test_types.set(test_type_ids)
        
        standard_ids = request.POST.getlist('standards')
        report.standards.set(standard_ids)
        
        test_result_ids = request.POST.getlist('test_results')
        report.test_results.set(test_result_ids)
        
        # 显示成功消息
        messages.success(request, '报告更新成功！')
        # 重定向到报告列表页面
        return redirect('report_list')
    
    # 渲染编辑报告模板
    return render(request, 'core/report_edit.html', {
        'report': report,
        'project_orders': project_orders,
        'clients': clients,
        'orders': orders,
        'staffs': staffs,
        'samples': samples,
        'standards': standards,
        'standard_radiation_hygiene': standard_radiation_hygiene,
        'test_results': test_results
    })


@login_required
def report_detail(request, pk):
    """报告详情视图函数"""
    # 获取指定ID的报告，不存在则返回404
    report = get_object_or_404(Report, pk=pk)
    # 获取报告关联的方案
    project_order = report.project_order
    # 获取本次方案自动生成的样品（仅关联当前方案的样品）
    samples = []
    if project_order:
        samples = project_order.samples.all()
    # 获取本次方案自动生成的测试（仅关联当前方案样品的测试）
    test_results = []
    if project_order:
        test_results = Test.objects.filter(sample__project_order=project_order)
    # 获取该方案关联的所有测试类型
    test_types = project_order.test_types.all() if project_order else []
    # 获取该方案关联的所有标准
    standards = project_order.standards.all() if project_order else []
    # 获取该方案关联的所有样品类型
    sample_types = project_order.sample_types.all() if project_order else []
    # 获取该方案关联的所有样品类型描述
    sample_type_descriptions = project_order.sample_type_descriptions.all() if project_order else []
    # 渲染报告详情模板
    return render(request, 'core/report_detail.html', {
        'report': report,
        'project_order': project_order,
        'samples': samples,
        'test_types': test_types,
        'standards': standards,
        'test_results': test_results,
        'sample_types': sample_types,
        'sample_type_descriptions': sample_type_descriptions
    })


def generate_pdf_report(request, pk):
    """生成PDF报告视图函数"""
    # 获取指定ID的报告，不存在则返回404
    report = get_object_or_404(Report, pk=pk)
    # 获取报告关联的方案
    project_order = report.project_order
    # 获取本次方案自动生成的样品（仅关联当前方案的样品）
    samples = []
    if project_order:
        samples = project_order.samples.all()
    # 获取本次方案自动生成的测试（仅关联当前方案样品的测试）
    test_results = []
    if project_order:
        test_results = Test.objects.filter(sample__project_order=project_order)
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
    try:
        html = HTML(string=html_string)
        pdf = html.write_pdf()
    except Exception as e:
        messages.error(request, f'PDF生成失败：{e}')
        return redirect('report_detail', pk=pk)
    
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


@login_required
@require_permission('can_manage_sample_descriptions')
def sample_type_description_list(request):
    """样品类型描述列表视图函数"""
    # 获取所有样品类型描述
    sample_type_descriptions = SampleTypeDescription.objects.all()
    # 渲染样品类型描述列表模板
    return render(request, 'core/sample_type_description_list.html', {'sample_type_descriptions': sample_type_descriptions})


@login_required
def sample_type_description_create(request):
    """添加样品类型描述视图函数"""
    # 获取所有样品类型
    sample_types = SampleType.objects.all()
    
    if request.method == 'POST':
        # 获取表单数据
        sample_type_id = request.POST['sample_type']
        description = request.POST['description']
        
        # 获取关联对象
        sample_type = SampleType.objects.get(pk=sample_type_id)
        
        # 创建样品类型描述对象
        sample_type_description = SampleTypeDescription(
            sample_type=sample_type,
            description=description,
            created_by=request.user
        )
        sample_type_description.save()
        
        # 显示成功消息
        messages.success(request, '样品类型描述添加成功！')
        # 重定向到样品类型描述列表页面
        return redirect('sample_type_description_list')
    
    # 渲染添加样品类型描述模板
    return render(request, 'core/sample_type_description_create.html', {'sample_types': sample_types})


@login_required
def sample_type_description_edit(request, pk):
    """编辑样品类型描述视图函数"""
    # 获取指定ID的样品类型描述，不存在则返回404
    sample_type_description = get_object_or_404(SampleTypeDescription, pk=pk)
    # 获取所有样品类型
    sample_types = SampleType.objects.all()
    
    if request.method == 'POST':
        # 获取表单数据
        sample_type_id = request.POST['sample_type']
        description = request.POST['description']
        
        # 获取关联对象
        sample_type = SampleType.objects.get(pk=sample_type_id)
        
        # 更新样品类型描述对象
        sample_type_description.sample_type = sample_type
        sample_type_description.description = description
        sample_type_description.save()
        
        # 显示成功消息
        messages.success(request, '样品类型描述更新成功！')
        # 重定向到样品类型描述列表页面
        return redirect('sample_type_description_list')
    
    # 渲染编辑样品类型描述模板
    return render(request, 'core/sample_type_description_edit.html', {
        'sample_type_description': sample_type_description,
        'sample_types': sample_types
    })


@login_required
def sample_type_description_delete(request, pk):
    """删除样品类型描述视图函数"""
    # 获取指定ID的样品类型描述，不存在则返回404
    sample_type_description = get_object_or_404(SampleTypeDescription, pk=pk)
    # 删除样品类型描述
    sample_type_description.delete()
    # 显示成功消息
    messages.success(request, '样品类型描述删除成功！')
    # 重定向到样品类型描述列表页面
    return redirect('sample_type_description_list')


@login_required
@require_permission('can_manage_sample_types')
def sample_type_list(request):
    """样品类型列表视图函数"""
    # 获取所有样品类型
    sample_types = SampleType.objects.all()
    # 渲染样品类型列表模板
    return render(request, 'core/sample_type_list.html', {'sample_types': sample_types})


@login_required
def sample_type_create(request):
    """添加样品类型视图函数"""
    if request.method == 'POST':
        # 获取表单数据
        name = request.POST['name']
        description = request.POST.get('description', '')
        
        # 创建样品类型对象
        sample_type = SampleType(
            name=name,
            description=description,
            created_by=request.user
        )
        sample_type.save()
        
        # 显示成功消息
        messages.success(request, '样品类型添加成功！')
        # 重定向到样品类型列表页面
        return redirect('sample_type_list')
    
    # 渲染添加样品类型模板
    return render(request, 'core/sample_type_create.html')


@login_required
def sample_type_edit(request, pk):
    """编辑样品类型视图函数"""
    # 获取指定ID的样品类型，不存在则返回404
    sample_type = get_object_or_404(SampleType, pk=pk)
    
    if request.method == 'POST':
        # 获取表单数据
        name = request.POST['name']
        description = request.POST.get('description', '')
        
        # 更新样品类型对象
        sample_type.name = name
        sample_type.description = description
        sample_type.save()
        
        # 显示成功消息
        messages.success(request, '样品类型更新成功！')
        # 重定向到样品类型列表页面
        return redirect('sample_type_list')
    
    # 渲染编辑样品类型模板
    return render(request, 'core/sample_type_edit.html', {'sample_type': sample_type})


@login_required
def sample_type_delete(request, pk):
    """删除样品类型视图函数"""
    sample_type = get_object_or_404(SampleType, pk=pk)
    if request.method == 'POST':
        sample_type.delete()
        messages.success(request, '样品类型已成功删除！')
    return redirect('sample_type_list')


def test_view(request):
    """测试视图函数"""
    return render(request, 'core/home.html')
