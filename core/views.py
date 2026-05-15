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
from .models import Client, Sample, Test, Order, Staff, Project_Order, Report, Department, SampleType, SampleTypeDescription, Position, ImportTemplate
from django.core.files.storage import FileSystemStorage
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

# 导入计算模块
from Calculation.cosmicRayResponseCalculation import calculate_r_gamma_avg_std, calculate_env_gamma, cosmicRayResponseCalculation


def create_tests_for_sample(sample):
    """
    为样品自动创建测试记录
    如果样品还没有测试记录，则创建一条
    """
    # 检查该样品是否已经有测试记录
    existing_tests = Test.objects.filter(sample=sample)
    if not existing_tests.exists():
        # 创建测试记录
        Test.objects.create(
            sample=sample,
            status='pending'
        )


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
def sample_list(request, project_id=None):
    """样品列表视图函数 - 支持按方案分页显示"""
    # 获取搜索关键词
    search_query = request.GET.get('search', '')
    
    # 获取所有方案（用于导航）
    all_projects = Project_Order.objects.all().order_by('project_id')
    
    # 获取当前方案信息
    current_project = None
    if project_id:
        try:
            current_project = Project_Order.objects.get(project_id=project_id)
        except Project_Order.DoesNotExist:
            project_id = None
    
    # 获取样品数据，使用select_related优化查询
    samples = Sample.objects.select_related(
        'client',
        'order',
        'sample_type',
        'project_order',
        'sample_type_description'
    )
    
    # 如果指定了方案，只显示该方案的样品
    if project_id:
        samples = samples.filter(project_order__project_id=project_id)
    
    # 按方案和样品描述排序
    samples = samples.order_by(
        'project_order__project_id',
        'sample_type_description__description'
    )
    
    # 如果有搜索关键词，进行模糊搜索
    if search_query:
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
    
    # 将样品按方案分组（如果没有指定方案），否则按样品描述分组
    grouped_samples = []
    
    if project_id and current_project:
        # 单方案模式：按样品描述分组
        descriptions = {}
        project_key = f"{current_project.project_id} - {current_project.name}"
        
        for sample in samples:
            sample_desc = sample.sample_type_description.description if sample.sample_type_description else "无描述"
            
            if sample_desc not in descriptions:
                descriptions[sample_desc] = []
            descriptions[sample_desc].append(sample)
        
        grouped_samples.append({
            'project_id': current_project.project_id,
            'project_name': project_key,
            'descriptions': descriptions
        })
    else:
        # 多方案模式：按方案分组，每个方案内再按样品描述分组
        current_project_key = None
        
        for sample in samples:
            project_order = sample.project_order
            proj_id = project_order.project_id if project_order else "无方案"
            proj_name = project_order.name if project_order else ""
            project_key = f"{proj_id} - {proj_name}" if project_order else "无方案"
            sample_desc = sample.sample_type_description.description if sample.sample_type_description else "无描述"
            
            # 如果是新的方案，添加新的方案组
            if current_project_key != project_key:
                grouped_samples.append({
                    'project_id': proj_id,
                    'project_name': project_key,
                    'descriptions': {}
                })
                current_project_key = project_key
            
            # 添加样品到对应的描述组
            current_group = grouped_samples[-1]
            if sample_desc not in current_group['descriptions']:
                current_group['descriptions'][sample_desc] = []
            current_group['descriptions'][sample_desc].append(sample)
    
    # 渲染样品列表模板
    return render(request, 'core/sample_list.html', {
        'grouped_samples': grouped_samples,
        'search_query': search_query,
        'all_projects': all_projects,
        'current_project_id': project_id,
        'current_project': current_project
    })


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
        
        # 为新创建的样品自动创建测试
        create_tests_for_sample(sample)
        
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
        
        # 为更新后的样品自动创建测试（如果还没有的话）
        create_tests_for_sample(sample)
        
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
def test_list(request, project_id=None):
    """测试列表视图函数 - 支持按方案分页显示"""
    # 获取搜索关键词
    search_query = request.GET.get('search', '')
    
    # 获取所有方案（用于导航）
    all_projects = Project_Order.objects.all().order_by('project_id')
    
    # 获取当前方案信息
    current_project = None
    if project_id:
        try:
            current_project = Project_Order.objects.get(project_id=project_id)
        except Project_Order.DoesNotExist:
            project_id = None
    
    # 获取测试数据，使用select_related优化查询
    tests = Test.objects.select_related(
        'sample', 
        'sample__sample_type', 
        'sample__project_order',
        'analyzed_by',
        'verified_by'
    ).prefetch_related(
        'sample__sample_type_description'
    )
    
    # 如果指定了方案，只显示该方案的测试
    if project_id:
        tests = tests.filter(sample__project_order__project_id=project_id)
    
    # 按方案和样品描述排序
    tests = tests.order_by(
        'sample__project_order__project_id',
        'sample__sample_type_description__description'
    )
    
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
    
    # 将测试按方案分组（如果没有指定方案），否则按样品描述分组
    grouped_tests = []
    
    if project_id and current_project:
        # 单方案模式：按样品描述分组
        descriptions = {}
        project_key = f"{current_project.project_id} - {current_project.name}"
        
        for test in tests:
            sample_desc = test.sample.sample_type_description.description if test.sample and test.sample.sample_type_description else "无描述"
            
            if sample_desc not in descriptions:
                descriptions[sample_desc] = []
            descriptions[sample_desc].append(test)
        
        grouped_tests.append({
            'project_id': current_project.project_id,
            'project_name': project_key,
            'descriptions': descriptions
        })
    else:
        # 多方案模式：按方案分组，每个方案内再按样品描述分组
        current_project_key = None
        
        for test in tests:
            project_order = test.sample.project_order if test.sample else None
            proj_id = project_order.project_id if project_order else "无方案"
            proj_name = project_order.name if project_order else ""
            project_key = f"{proj_id} - {proj_name}" if project_order else "无方案"
            sample_desc = test.sample.sample_type_description.description if test.sample and test.sample.sample_type_description else "无描述"
            
            # 如果是新的方案，添加新的方案组
            if current_project_key != project_key:
                grouped_tests.append({
                    'project_id': proj_id,
                    'project_name': project_key,
                    'descriptions': {}
                })
                current_project_key = project_key
            
            # 添加测试到对应的描述组
            current_group = grouped_tests[-1]
            if sample_desc not in current_group['descriptions']:
                current_group['descriptions'][sample_desc] = []
            current_group['descriptions'][sample_desc].append(test)
    
    # 渲染测试列表模板
    return render(request, 'core/test_list.html', {
        'grouped_tests': grouped_tests, 
        'search_query': search_query,
        'all_projects': all_projects,
        'current_project_id': project_id,
        'current_project': current_project
    })


@login_required
@require_permission('can_manage_tests')
def save_radiation_info(request):
    """保存辐射测量基本信息和宇宙射线信息"""
    if request.method == 'POST':
        import json
        project_id = request.POST.get('project_id', '')
        
        try:
            # 使用 select_for_update 锁定记录，防止并发问题
            project_order = Project_Order.objects.select_for_update().get(project_id=project_id)
            
            # 批量更新字段，减少数据库操作
            update_fields = {}
            update_fields['radiation_project_name'] = request.POST.get('radiation_project_name', '')
            update_fields['radiation_monitoring_date'] = request.POST.get('radiation_monitoring_date', '')
            update_fields['radiation_location'] = request.POST.get('radiation_location', '')
            update_fields['radiation_weather'] = request.POST.get('radiation_weather', '')
            update_fields['radiation_basis'] = request.POST.get('radiation_basis', '')
            update_fields['radiation_temperature'] = request.POST.get('radiation_temperature', '')
            update_fields['radiation_humidity'] = request.POST.get('radiation_humidity', '')
            update_fields['radiation_conditions'] = request.POST.get('radiation_conditions', '')
            
            # 保存宇宙射线信息（JSON 格式）
            cosmic_ray_str = request.POST.get('cosmic_ray_info', '[]')
            try:
                cosmic_ray_info = json.loads(cosmic_ray_str)
                update_fields['cosmic_ray_info'] = cosmic_ray_info
            except Exception as e:
                print(f"Error parsing cosmic_ray_info: {e}")
            
            # 保存仪器信息（JSON 格式）
            instrument_str = request.POST.get('instrument_info', '[]')
            try:
                instrument_info = json.loads(instrument_str)
                update_fields['instrument_info'] = instrument_info
            except Exception as e:
                print(f"Error parsing instrument_info: {e}")
            
            # 使用 update 方法批量更新，只更新修改的字段
            for field, value in update_fields.items():
                setattr(project_order, field, value)
            
            # 只保存必要的字段
            project_order.save(update_fields=list(update_fields.keys()))
            
            # 返回完整的数据对象供前端更新显示
            return JsonResponse({
                'success': True,
                'message': '保存成功',
                'radiation_project_name': project_order.radiation_project_name,
                'radiation_monitoring_date': project_order.radiation_monitoring_date,
                'radiation_location': project_order.radiation_location,
                'radiation_weather': project_order.radiation_weather,
                'radiation_basis': project_order.radiation_basis,
                'radiation_temperature': project_order.radiation_temperature,
                'radiation_humidity': project_order.radiation_humidity,
                'radiation_conditions': project_order.radiation_conditions,
                'cosmic_ray_info': project_order.cosmic_ray_info,
                'instrument_info': project_order.instrument_info
            })
        except Project_Order.DoesNotExist:
            return JsonResponse({'success': False, 'message': '方案不存在'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'保存失败：{str(e)}'})
    
    return JsonResponse({'success': False, 'message': '请求方法错误'})


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
        unit = request.POST.get('unit', '')
        analyzed_by_id = request.POST.get('analyzed_by')
        verified_by_id = request.POST.get('verified_by')
        analysis_date = request.POST.get('analysis_date')
        verification_date = request.POST.get('verification_date')
        
        # 获取样品对象
        sample = Sample.objects.get(pk=sample_id)
        
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
            status=status,
            analyzed_by=analyzed_by,
            verified_by=verified_by,
            analysis_date=analysis_date if analysis_date else None,
            verification_date=verification_date if verification_date else None,
            address=request.POST.get('address', '')
        )
        # 使用 set_result_with_unit 方法设置结果和单位（会自动计算基础值）
        test.set_result_with_unit(result, unit)
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
        unit = request.POST.get('unit', '')
        analyzed_by_id = request.POST.get('analyzed_by')
        verified_by_id = request.POST.get('verified_by')
        analysis_date = request.POST.get('analysis_date')
        verification_date = request.POST.get('verification_date')
        
        # 获取样品对象
        sample = Sample.objects.get(pk=sample_id)
        
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
        test.status = status
        # 使用 set_result_with_unit 方法设置结果和单位（会自动计算基础值）
        test.set_result_with_unit(result, unit)
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
                    sample = Sample.objects.create(
                        client=client,
                        order=order,
                        project_order=project_order,
                        sample_type=sample_type_description.sample_type,
                        sample_type_description=sample_type_description,
                        collection_date=datetime.now()
                    )
                    # 为新创建的样品自动创建测试
                    create_tests_for_sample(sample)
            except SampleTypeDescription.DoesNotExist:
                pass
        
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
                    sample = Sample.objects.create(
                        client=client,
                        order=order,
                        project_order=project_order,
                        sample_type=sample_type_description.sample_type,
                        sample_type_description=sample_type_description,
                        collection_date=datetime.now()
                    )
                    # 为新创建的样品自动创建测试
                    create_tests_for_sample(sample)
            except SampleTypeDescription.DoesNotExist:
                pass
        
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
        'standards': standards
    })


#方案详情视图函数
@login_required
def project_order_detail(request, pk):
    """项目方案详情视图函数 - 通过主键查询"""
    # 尝试先按主键查询，如果失败则按 project_id 查询
    try:
        # 尝试按主键查询（整数），使用 only() 只选择需要的字段
        project_order = Project_Order.objects.only(
            'radiation_project_name', 'radiation_monitoring_date', 'radiation_location',
            'radiation_weather', 'radiation_basis', 'radiation_temperature', 'radiation_humidity',
            'radiation_conditions', 'cosmic_ray_info', 'instrument_info'
        ).get(pk=pk)
    except Project_Order.DoesNotExist:
        # 如果主键查询失败，尝试按 project_id 查询（字符串）
        try:
            project_order = Project_Order.objects.only(
                'radiation_project_name', 'radiation_monitoring_date', 'radiation_location',
                'radiation_weather', 'radiation_basis', 'radiation_temperature', 'radiation_humidity',
                'radiation_conditions', 'cosmic_ray_info', 'instrument_info'
            ).get(project_id=pk)
        except Project_Order.DoesNotExist:
            return JsonResponse({'error': '方案不存在'}, status=404)
    
    # 如果是 AJAX 请求，返回 JSON 数据
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.headers.get('Accept', '').find('application/json') != -1:
        data = {
            'radiation_project_name': project_order.radiation_project_name,
            'radiation_monitoring_date': project_order.radiation_monitoring_date,
            'radiation_location': project_order.radiation_location,
            'radiation_weather': project_order.radiation_weather,
            'radiation_basis': project_order.radiation_basis,
            'radiation_temperature': project_order.radiation_temperature,
            'radiation_humidity': project_order.radiation_humidity,
            'radiation_conditions': project_order.radiation_conditions,
            'cosmic_ray_info': project_order.cosmic_ray_info or [],
            'instrument_info': project_order.instrument_info or []
        }
        return JsonResponse(data)
    
    # 获取该方案关联的所有样品类型描述
    sample_type_descriptions = project_order.sample_type_descriptions.all()
    # 获取该方案关联的所有标准
    standards = project_order.standards.all()
    
    # 获取样品描述数量信息
    sample_type_description_quantities = project_order.sample_type_description_quantities or {}
    
    # 渲染项目方案详情模板
    return render(request, 'core/project_order_detail.html', {
        'project_order': project_order,
        'sample_type_descriptions': sample_type_descriptions,
        'sample_type_description_quantities': sample_type_description_quantities,
        'standards': standards
    })


@login_required
def project_order_detail_by_id(request, project_id):
    """项目方案详情视图函数 - 通过项目ID字符串查询（用于AJAX请求）"""
    try:
        project_order = Project_Order.objects.only(
            'radiation_project_name', 'radiation_monitoring_date', 'radiation_location',
            'radiation_weather', 'radiation_basis', 'radiation_temperature', 'radiation_humidity',
            'radiation_conditions', 'cosmic_ray_info', 'instrument_info'
        ).get(project_id=project_id)
        
        # 返回JSON数据
        data = {
            'radiation_project_name': project_order.radiation_project_name,
            'radiation_monitoring_date': project_order.radiation_monitoring_date,
            'radiation_location': project_order.radiation_location,
            'radiation_weather': project_order.radiation_weather,
            'radiation_basis': project_order.radiation_basis,
            'radiation_temperature': project_order.radiation_temperature,
            'radiation_humidity': project_order.radiation_humidity,
            'radiation_conditions': project_order.radiation_conditions,
            'cosmic_ray_info': project_order.cosmic_ray_info or [],
            'instrument_info': project_order.instrument_info or []
        }
        return JsonResponse(data)
        
    except Project_Order.DoesNotExist:
        return JsonResponse({'error': '方案不存在'}, status=404)


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
    # 获取所有标准（测试类型）
    standards = Standard.objects.all()
    # 获取所有标准（标准）
    standard_radiation_hygiene = Standard_radiation_hygiene.objects.all()
    
    # 根据报告关联的方案获取相关的样品和测试
    if report.project_order:
        # 获取方案关联的样品
        samples = Sample.objects.filter(project_order=report.project_order)
        # 获取这些样品关联的测试
        test_results = Test.objects.filter(sample__in=samples)
    else:
        # 如果没有关联方案，显示空列表
        samples = Sample.objects.none()
        test_results = Test.objects.none()
    
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
    # 获取该方案关联的所有标准
    standards = project_order.standards.all() if project_order else []
    # 获取该方案关联的所有样品类型描述
    sample_type_descriptions = project_order.sample_type_descriptions.all() if project_order else []
    # 渲染报告详情模板
    return render(request, 'core/report_detail.html', {
        'report': report,
        'project_order': project_order,
        'samples': samples,
        'standards': standards,
        'test_results': test_results,
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
    # 获取该方案关联的所有标准
    standards = project_order.standards.all() if project_order else []
    
    # 渲染HTML模板
    html_string = render_to_string('core/report_pdf.html', {
        'report': report,
        'project_order': project_order,
        'samples': samples,
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
        unit = request.POST.get('unit', '')
        
        # 获取关联对象
        sample_type = SampleType.objects.get(pk=sample_type_id)
        
        # 创建样品类型描述对象
        sample_type_description = SampleTypeDescription(
            sample_type=sample_type,
            description=description,
            unit=unit,
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
        unit = request.POST.get('unit', '')
        
        # 获取关联对象
        sample_type = SampleType.objects.get(pk=sample_type_id)
        
        # 更新样品类型描述对象
        sample_type_description.sample_type = sample_type
        sample_type_description.description = description
        sample_type_description.unit = unit
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


@login_required
@require_permission('can_manage_tests')
def test_import_excel(request):
    """测试数据Excel批量导入视图函数"""
    if request.method == 'POST':
        import pandas as pd
        from io import BytesIO
        
        # 获取上传的Excel文件
        excel_file = request.FILES.get('excel_file')
        project_name = request.POST.get('project_name', '')
        description = request.POST.get('description', '')
        import_mode = request.POST.get('import_mode', 'update')
        
        if not excel_file:
            messages.error(request, '请选择要导入的Excel文件！')
            return redirect('test_list')
        
        try:
            # 读取Excel文件
            excel_data = BytesIO(excel_file.read())
            
            # 判断是否为辐射剂量率类型的描述
            is_radiation = False
            
            # 方式1：从表单描述判断
            if description and ('辐射' in description or 'γ' in description or 'X射线' in description or 'x射线' in description.lower()):
                is_radiation = True
            
            # 方式2：从Excel文件检测（即使描述为空也能识别）
            if not is_radiation:
                try:
                    excel_data.seek(0)
                    xls = pd.ExcelFile(excel_data)
                    sheet_names = xls.sheet_names
                    
                    # 检查是否有"基本信息"工作表
                    if '基本信息' in sheet_names:
                        is_radiation = True
                    else:
                        # 检查第一个工作表是否包含辐射相关列
                        first_sheet = pd.read_excel(xls, sheet_name=sheet_names[0], header=0, nrows=0)
                        cols = [str(c).strip() for c in first_sheet.columns]
                        radiation_cols = ['点位描述', '仪器示值', 'Rγ', '宇宙射线', 'k3', '经度', '纬度', '高程']
                        for col in cols:
                            if any(keyword in col for keyword in radiation_cols):
                                is_radiation = True
                                break
                except Exception:
                    pass
            
            # 根据是否为辐射类型选择必需的列
            if is_radiation:
                # 辐射剂量率类型必需的列（支持"样本ID"或"序号"作为样本标识）
                required_columns = ['点位描述', '经度（E）', '纬度（N）', '高程（H）', 
                                   '仪器示值Rγ(1)', '仪器示值Rγ(2)', '仪器示值Rγ(3)', 
                                   '仪器示值Rγ(4)', '仪器示值Rγ(5)', '宇宙射线', 'k3', '平均值', '标准差', '备注']
            else:
                # 普通类型必需的列
                required_columns = ['样本ID', '结果', '地址信息', '分析人员', '分析日期']
            
            # 尝试读取Excel文件，优先查找包含所需列的工作表
            df = None
            cosmic_ray_info = []
            instrument_info = []
            basic_info = {}
            
            try:
                excel_data.seek(0)
                xls = pd.ExcelFile(excel_data)
                sheet_names = xls.sheet_names
                
                # 如果是辐射类型，先读取"基本信息"工作表获取共同信息、宇宙射线信息和仪器信息
                if is_radiation:
                    if '基本信息' in sheet_names:
                        basic_info_df = pd.read_excel(xls, sheet_name='基本信息', header=None)
                        
                        # 解析基本信息（项目名称、监测日期等）
                        in_cosmic_ray_section = False
                        in_instrument_section = False
                        cosmic_ray_header = None
                        instrument_header = None
                        
                        for i in range(len(basic_info_df)):
                            row = basic_info_df.iloc[i]
                            
                            # 检测宇宙射线信息区域
                            if '宇宙射线信息' in str(row[0]):
                                in_cosmic_ray_section = True
                                in_instrument_section = False
                                continue
                            
                            # 检测仪器信息区域
                            if '仪器信息' in str(row[0]):
                                in_instrument_section = True
                                in_cosmic_ray_section = False
                                continue
                            
                            # 检测空行，结束当前区域
                            if pd.isna(row[0]) or str(row[0]).strip() == '':
                                if in_cosmic_ray_section and cosmic_ray_header:
                                    in_cosmic_ray_section = False
                                if in_instrument_section and instrument_header:
                                    in_instrument_section = False
                                continue
                            
                            # 处理基本信息
                            if not in_cosmic_ray_section and not in_instrument_section:
                                if len(row) >= 2:
                                    key = str(row[0]).strip()
                                    value = str(row[1]).strip() if pd.notna(row[1]) else ''
                                    if key and key != 'nan' and value and value != 'nan':
                                        # 匹配基本信息字段（使用更宽松的匹配方式）
                                        if '项目名称' in key:
                                            basic_info['radiation_project_name'] = value
                                        elif '监测日期' in key:
                                            basic_info['radiation_monitoring_date'] = value
                                        elif '监测地点' in key:
                                            basic_info['radiation_location'] = value
                                        elif '天气状况' in key:
                                            basic_info['radiation_weather'] = value
                                        elif '监测依据' in key:
                                            basic_info['radiation_basis'] = value
                                        elif '温度' in key:
                                            basic_info['radiation_temperature'] = value
                                        elif '湿度' in key:
                                            basic_info['radiation_humidity'] = value
                                        elif '测量工况' in key:
                                            basic_info['radiation_conditions'] = value
                            
                            # 处理宇宙射线信息
                            elif in_cosmic_ray_section:
                                # 第一行作为表头
                                if cosmic_ray_header is None:
                                    cosmic_ray_header = [str(x).strip() for x in row.dropna().values]
                                else:
                                    # 读取数据行，转换为前端期望的字段名
                                    item = {}
                                    has_data = False
                                    for j, col_name in enumerate(cosmic_ray_header):
                                        if j < len(row):
                                            value = str(row[j]).strip() if pd.notna(row[j]) else ''
                                            # 转换字段名为前端期望的格式
                                            if '测量地点' in col_name:
                                                item['location'] = value
                                            elif '经度' in col_name:
                                                item['longitude'] = value
                                            elif '纬度' in col_name:
                                                item['latitude'] = value
                                            elif '高程' in col_name:
                                                item['elevation'] = value
                                            elif '响应值' in col_name or 'Xc' in col_name:
                                                item['xc_response'] = value
                                            elif col_name == '编号':
                                                item['id'] = value
                                            else:
                                                item[col_name] = value
                                    # 检查是否有除编号外的实际数据
                                    if item.get('location') or item.get('longitude') or item.get('latitude') or item.get('elevation') or item.get('xc_response'):
                                        cosmic_ray_info.append(item)
                            
                            # 处理仪器信息
                            elif in_instrument_section:
                                # 第一行作为表头
                                if instrument_header is None:
                                    instrument_header = [str(x).strip() for x in row.dropna().values]
                                else:
                                    # 读取数据行，转换为前端期望的字段名
                                    item = {}
                                    for j, col_name in enumerate(instrument_header):
                                        if j < len(row):
                                            value = str(row[j]).strip() if pd.notna(row[j]) else ''
                                            # 转换字段名为前端期望的格式
                                            if '名称' in col_name:
                                                item['name'] = value
                                            elif '型号' in col_name:
                                                item['model'] = value
                                            elif '编号' in col_name:
                                                # 第二个编号字段作为code
                                                if 'code' not in item:
                                                    item['id'] = value
                                                else:
                                                    item['code'] = value
                                            elif 'k1' in col_name or '校准' in col_name or '检定' in col_name:
                                                item['k1'] = value
                                            elif 'k2' in col_name or '效率' in col_name:
                                                item['k2'] = value
                                            else:
                                                item[col_name] = value
                                    # 检查是否有除编号外的实际数据
                                    if item.get('name') or item.get('model') or item.get('code') or item.get('k1') or item.get('k2'):
                                        instrument_info.append(item)
                
                # 首先尝试读取第一个工作表
                df = pd.read_excel(excel_data)
                missing_columns = [col for col in required_columns if col not in df.columns]
                
                # 如果第一个工作表缺少必需的列，尝试查找其他工作表
                if missing_columns and is_radiation:
                    excel_data.seek(0)
                    xls = pd.ExcelFile(excel_data)
                    
                    # 尝试查找"测量记录"工作表（模板文件格式）
                    if '测量记录' in sheet_names:
                        # 首先尝试不指定header，手动处理表头
                        temp_df_raw = pd.read_excel(xls, sheet_name='测量记录', header=None)
                        # 查找包含"序号"的行作为表头行（通常在第一行或第二行）
                        header_row_index = -1
                        for i in range(min(5, len(temp_df_raw))):
                            if '序号' in str(temp_df_raw.iloc[i, 0]):
                                header_row_index = i
                                break
                        
                        if header_row_index >= 0:
                            # 使用找到的表头行，从下一行开始读取数据
                            new_header = temp_df_raw.iloc[header_row_index]
                            df = temp_df_raw[header_row_index+1:]
                            df.columns = new_header
                            missing_columns = [col for col in required_columns if col not in df.columns]
                        else:
                            # 如果没找到，尝试默认方式
                            temp_df = pd.read_excel(xls, sheet_name='测量记录', header=0)
                            temp_missing = [col for col in required_columns if col not in temp_df.columns]
                            if not temp_missing:
                                df = temp_df
                                missing_columns = []
                    
                    # 如果还是没有找到，尝试查找"测量数据"工作表
                    if missing_columns and '测量数据' in sheet_names:
                        df = pd.read_excel(xls, sheet_name='测量数据')
                        missing_columns = [col for col in required_columns if col not in df.columns]
                    
                    # 如果都没有，检查所有工作表
                    if missing_columns:
                        for sheet_name in sheet_names:
                            temp_df = pd.read_excel(xls, sheet_name=sheet_name)
                            temp_missing = [col for col in required_columns if col not in temp_df.columns]
                            if not temp_missing:
                                df = temp_df
                                missing_columns = []
                                break
            except Exception as e:
                messages.error(request, f'读取Excel文件失败：{str(e)}')
                return redirect('test_list')
            
            if df is None:
                messages.error(request, '无法读取Excel文件')
                return redirect('test_list')
            
            if missing_columns:
                messages.error(request, f'Excel文件缺少必需的列：{", ".join(missing_columns)}')
                return redirect('test_list')
            
            # 解析方案ID
            project_id = project_name.split(' - ')[0] if ' - ' in project_name else project_name
            
            # 获取方案对象
            project_order = None
            if project_id:
                try:
                    project_order = Project_Order.objects.get(project_id=project_id)
                except Project_Order.DoesNotExist:
                    messages.error(request, f'方案 {project_id} 不存在！')
                    return redirect('test_list')
            
            # 统计导入结果
            success_count = 0
            error_count = 0
            error_messages = []
            
            # 遍历Excel数据
            for index, row in df.iterrows():
                try:
                    if is_radiation:
                        # 辐射剂量率类型的数据处理
                        # 支持"样本ID"或"序号"作为样本标识列
                        # 使用更宽松的列名匹配方式（去除空格和特殊字符）
                        sample_id = ''
                        for col in df.columns:
                            col_clean = str(col).strip()
                            if col_clean == '样本ID' or col_clean == '序号':
                                sample_id = str(row[col]).strip() if pd.notna(row[col]) else ''
                                break
                            
                        # 获取各字段值，使用宽松匹配
                        def get_value(col_name):
                            for col in df.columns:
                                if col_name in str(col) or (col_name.replace(' ', '') in str(col).replace(' ', '')):
                                    return str(row[col]).strip() if pd.notna(row[col]) else ''
                            return ''
                            
                        point_desc = get_value('点位描述')
                        longitude = get_value('经度')
                        latitude = get_value('纬度')
                        elevation = get_value('高程')
                        r1 = get_value('仪器示值Rγ(1)')
                        r2 = get_value('仪器示值Rγ(2)')
                        r3 = get_value('仪器示值Rγ(3)')
                        r4 = get_value('仪器示值Rγ(4)')
                        r5 = get_value('仪器示值Rγ(5)')
                        cosmic_ray = get_value('宇宙射线')
                        k3 = get_value('k3')
                        avg_value = get_value('平均值')
                        std_value = get_value('标准差')
                        remark = get_value('备注')
                        
                        # 使用平均值作为结果
                        result = avg_value
                        # 使用点位描述作为地址信息
                        address = point_desc
                    else:
                        # 普通类型的数据处理
                        sample_id = str(row['样本ID']).strip()
                        result = str(row['结果']) if pd.notna(row['结果']) else ''
                        address = str(row['地址信息']) if pd.notna(row['地址信息']) else ''
                   
                    analyzed_by_username = str(row['分析人员']) if pd.notna(row.get('分析人员')) else ''
                    analysis_date_str = str(row['分析日期']) if pd.notna(row.get('分析日期')) else ''
                    
                    # 查找样本
                    sample = None
                    try:
                        # 首先尝试直接匹配样本ID
                        sample = Sample.objects.get(sample_id=sample_id, project_order=project_order)
                    except Sample.DoesNotExist:
                        # 如果直接匹配失败，对于辐射类型，尝试将序号转换为样本ID格式
                        if is_radiation and sample_id.isdigit():
                            # 获取方案下的所有样本，按ID排序
                            project_samples = list(Sample.objects.filter(project_order=project_order).order_by('sample_id'))
                            # 根据序号索引查找样本（序号从1开始）
                            try:
                                sample = project_samples[int(sample_id) - 1]
                            except IndexError:
                                pass
                    
                    if not sample:
                        error_count += 1
                        error_messages.append(f'第{index + 2}行：样本 {sample_id} 不存在')
                        continue
                    
                    # 验证样品描述是否匹配
                    if description != "无描述" and sample.sample_type_description:
                        if sample.sample_type_description.description != description:
                            error_count += 1
                            error_messages.append(f'第{index + 2}行：样本 {sample_id} 的样品描述不匹配')
                            continue
                    
                    # 查找或创建测试
                    if import_mode == 'create':
                        # 创建新模式：创建新测试
                        test = Test(
                            sample=sample,
                            result=result,
                            address=address,
                            status='completed'
                        )
                    else:
                        # 更新模式：查找现有测试
                        try:
                            test = Test.objects.get(sample=sample)
                            test.result = result
                            test.address = address
                            test.status = 'completed'
                        except Test.DoesNotExist:
                            # 如果不存在则创建
                            test = Test(
                                sample=sample,
                                result=result,
                                address=address,
                                status='completed'
                            )
                    
                    # 设置分析人员
                    if analyzed_by_username:
                        try:
                            analyzed_by = User.objects.get(username=analyzed_by_username)
                            test.analyzed_by = analyzed_by
                        except User.DoesNotExist:
                            pass
                    
                    # 设置分析日期
                    if analysis_date_str:
                        try:
                            from datetime import datetime
                            # 尝试多种日期格式
                            for fmt in ['%Y-%m-%d %H:%M', '%Y-%m-%d', '%Y/%m/%d %H:%M', '%Y/%m/%d']:
                                try:
                                    test.analysis_date = datetime.strptime(analysis_date_str, fmt)
                                    break
                                except ValueError:
                                    continue
                        except:
                            pass
                    
                    # 如果是辐射剂量率类型，设置专用字段
                    if is_radiation:
                        test.point_description = point_desc
                        # 将字符串转换为数值类型
                        try:
                            test.longitude = float(longitude) if longitude else None
                        except ValueError:
                            test.longitude = None
                        try:
                            test.latitude = float(latitude) if latitude else None
                        except ValueError:
                            test.latitude = None
                        try:
                            test.elevation = float(elevation) if elevation else None
                        except ValueError:
                            test.elevation = None
                        try:
                            test.r_gamma_1 = float(r1) if r1 else None
                        except ValueError:
                            test.r_gamma_1 = None
                        try:
                            test.r_gamma_2 = float(r2) if r2 else None
                        except ValueError:
                            test.r_gamma_2 = None
                        try:
                            test.r_gamma_3 = float(r3) if r3 else None
                        except ValueError:
                            test.r_gamma_3 = None
                        try:
                            test.r_gamma_4 = float(r4) if r4 else None
                        except ValueError:
                            test.r_gamma_4 = None
                        try:
                            test.r_gamma_5 = float(r5) if r5 else None
                        except ValueError:
                            test.r_gamma_5 = None
                        try:
                            test.cosmic_ray = float(cosmic_ray) if cosmic_ray else None
                        except ValueError:
                            test.cosmic_ray = None
                        try:
                            test.k3 = float(k3) if k3 else None
                        except ValueError:
                            test.k3 = None
                        try:
                            test.avg_value = float(avg_value) if avg_value else None
                        except ValueError:
                            test.avg_value = None
                        try:
                            test.std_value = float(std_value) if std_value else None
                        except ValueError:
                            test.std_value = None
                        test.remark = remark
                    
                        # 自动计算平均值、标准差和环境γ辐射剂量率
                        if is_radiation:
                            # 获取5次仪器示值
                            r_vals = [test.r_gamma_1, test.r_gamma_2, test.r_gamma_3, test.r_gamma_4, test.r_gamma_5]
                            
                            # 检查是否有有效的仪器示值
                            valid_r = [v for v in r_vals if v is not None]
                            if len(valid_r) >= 2:
                                # 使用计算模块计算平均值和标准差
                                calc_avg, calc_std = calculate_r_gamma_avg_std(
                                    test.r_gamma_1 or 0,
                                    test.r_gamma_2 or 0,
                                    test.r_gamma_3 or 0,
                                    test.r_gamma_4 or 0,
                                    test.r_gamma_5 or 0
                                )
                                
                                # 总是使用计算值覆盖（即使Excel中有值）
                                test.avg_value = calc_avg
                                test.std_value = calc_std
                                
                                # 计算环境γ辐射剂量率
                                # 获取仪器参数（优先从project_order，其次从basic_info）
                                k1 = 1.0
                                k2 = 1.0
                                
                                # 方式1：从project_order.instrument_info获取
                                if project_order and hasattr(project_order, 'instrument_info') and project_order.instrument_info:
                                    instrument_info_data = project_order.instrument_info
                                    if isinstance(instrument_info_data, list) and len(instrument_info_data) > 0:
                                        k1 = float(instrument_info_data[0].get('k1', 1.0))
                                        k2 = float(instrument_info_data[0].get('k2', 1.0))
                                
                                # 计算宇宙射线响应值
                                # 如果有经纬度和高程，使用计算模块计算
                                calculated_xc = None
                                if test.longitude and test.latitude and test.elevation:
                                    try:
                                        # 使用基准点参数计算宇宙射线响应值
                                        # 参数：经度, 纬度, 高程, r_gamma_1~5, cosmic_ray_HONG_0, cosmic_ray, cosmic_ray_Hong, k3, xc_response, xc_response_1, SinlanmudaM, lanmudaM
                                        calculated_xc = cosmicRayResponseCalculation(
                                            test.longitude,
                                            test.latitude,
                                            test.elevation,
                                            test.r_gamma_1 or 0,
                                            test.r_gamma_2 or 0,
                                            test.r_gamma_3 or 0,
                                            test.r_gamma_4 or 0,
                                            test.r_gamma_5 or 0,
                                            30,      # cosmic_ray_HONG_0
                                            0,       # cosmic_ray
                                            42.31795062,  # cosmic_ray_Hong
                                            k3_val,  # k3
                                            13,      # xc_response (基准点响应值)
                                            0,       # xc_response_1
                                            0,       # SinlanmudaM
                                            0        # lanmudaM
                                        )
                                    except Exception as calc_e:
                                        print(f"计算宇宙射线响应值失败: {calc_e}")
                                
                                # 优先使用计算值，其次使用Excel中的值
                                xc_response = calculated_xc if calculated_xc else (test.cosmic_ray or 0)
                                
                                # 更新test的cosmic_ray字段为计算值
                                if calculated_xc:
                                    test.cosmic_ray = calculated_xc
                                
                                # 获取屏蔽修正因子
                                k3_val = test.k3 or 1.0
                                
                                # 计算环境γ辐射剂量率
                                env_gamma_val = calculate_env_gamma(
                                    None,          # env_gamma参数（输出）
                                    xc_response,   # xc_response_1
                                    k3_val,        # k3
                                    k1,            # k1
                                    k2,            # k2
                                    test.avg_value # avg
                                )
                                
                                # 将计算结果保存为测试结果
                                if env_gamma_val is not None:
                                    test.result = str(round(env_gamma_val, 4))
                    
                    test.save()
                    success_count += 1
                    
                except Exception as e:
                    error_count += 1
                    error_messages.append(f'第{index + 2}行：{str(e)}')
            
            # 如果是辐射类型且有基本信息，保存到项目方案
            if is_radiation and project_order:
                try:
                    # 使用 select_for_update 锁定记录，防止并发问题
                    project_order = Project_Order.objects.select_for_update().get(pk=project_order.pk)
                    
                    # 批量更新字段
                    update_fields = []
                    
                    # 保存基本信息
                    if 'radiation_project_name' in basic_info:
                        project_order.radiation_project_name = basic_info['radiation_project_name']
                        update_fields.append('radiation_project_name')
                    if 'radiation_monitoring_date' in basic_info:
                        project_order.radiation_monitoring_date = basic_info['radiation_monitoring_date']
                        update_fields.append('radiation_monitoring_date')
                    if 'radiation_location' in basic_info:
                        project_order.radiation_location = basic_info['radiation_location']
                        update_fields.append('radiation_location')
                    if 'radiation_weather' in basic_info:
                        project_order.radiation_weather = basic_info['radiation_weather']
                        update_fields.append('radiation_weather')
                    if 'radiation_basis' in basic_info:
                        project_order.radiation_basis = basic_info['radiation_basis']
                        update_fields.append('radiation_basis')
                    if 'radiation_temperature' in basic_info:
                        project_order.radiation_temperature = basic_info['radiation_temperature']
                        update_fields.append('radiation_temperature')
                    if 'radiation_humidity' in basic_info:
                        project_order.radiation_humidity = basic_info['radiation_humidity']
                        update_fields.append('radiation_humidity')
                    if 'radiation_conditions' in basic_info:
                        project_order.radiation_conditions = basic_info['radiation_conditions']
                        update_fields.append('radiation_conditions')
                    
                    # 保存宇宙射线信息（总是保存，包括空列表，以清空旧数据）
                    project_order.cosmic_ray_info = cosmic_ray_info
                    update_fields.append('cosmic_ray_info')
                    
                    # 保存仪器信息（总是保存，包括空列表，以清空旧数据）
                    project_order.instrument_info = instrument_info
                    update_fields.append('instrument_info')
                    
                    if update_fields:
                        project_order.save(update_fields=update_fields)
                        messages.info(request, '成功保存辐射测量基本信息、宇宙射线信息和仪器信息！')
                except Exception as e:
                    messages.warning(request, f'保存辐射测量信息失败：{str(e)}')
            
            # 显示导入结果
            if success_count > 0:
                messages.success(request, f'成功导入 {success_count} 条测试数据！')
            if error_count > 0:
                messages.warning(request, f'导入失败 {error_count} 条，前5条错误：{"; ".join(error_messages[:5])}')
        
        except Exception as e:
            messages.error(request, f'导入失败：{str(e)}')
        
        return redirect('test_list')
    
    return redirect('test_list')


@login_required
@require_permission('can_manage_tests')
def test_import_template(request):
    """下载测试数据导入模板"""
    import pandas as pd
    from io import BytesIO
    import os
    
    # 获取查询参数
    project_name = request.GET.get('project', '')
    description = request.GET.get('description', '')
    
    # 解析方案ID
    project_id = project_name.split(' - ')[0] if ' - ' in project_name else project_name
    
    # 判断是否为辐射剂量率类型的描述
    is_radiation = False
    if description and ('辐射' in description or 'γ' in description or 'X射线' in description or 'x射线' in description.lower()):
        is_radiation = True
    
    # 如果是辐射类型，返回现成的模板文件
    if is_radiation:
        # 使用相对路径，基于项目根目录
        import senaite_lims.settings as settings
        template_path = os.path.join(settings.BASE_DIR, '导入资料', '环境γ辐射剂量率测量记录表.xlsx')
        
        if os.path.exists(template_path):
            # 读取现成的模板文件
            with open(template_path, 'rb') as f:
                template_content = f.read()
            
            response = HttpResponse(
                template_content,
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = f'attachment; filename="环境γ辐射剂量率测量记录表_{project_id}_{description}.xlsx"'
            return response
    
    # 普通类型模板
    data = {
        '样本ID': ['示例：SAMPLE-20240506-0001'],
        '结果': ['0.85'],
        '地址信息': ['西安市高新区'],
        '分析人员': ['zhangsan'],
        '分析日期': ['2024-05-06 10:30']
    }
    
    # 如果指定了方案和描述，获取对应的样本列表
    if project_id and description:
        try:
            project_order = Project_Order.objects.get(project_id=project_id)
            samples = Sample.objects.filter(
                project_order=project_order,
                sample_type_description__description=description
            )
            
            if samples.exists():
                data = {
                    '样本ID': [s.sample_id for s in samples],
                    '结果': [''] * len(samples),
                    '地址信息': [''] * len(samples),
                    '分析人员': [''] * len(samples),
                    '分析日期': [''] * len(samples)
                }
        except:
            pass
    
    # 创建DataFrame
    df = pd.DataFrame(data)
    
    # 创建Excel文件
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='测量数据')
        
        # 获取工作表
        worksheet = writer.sheets['测量数据']
        
        # 调整列宽
        column_widths = {'A': 30, 'B': 15, 'C': 40, 'D': 15, 'E': 20}
        
        for col, width in column_widths.items():
            worksheet.column_dimensions[col].width = width
    
    output.seek(0)
    
    # 设置响应头
    response = HttpResponse(
        output.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="测试数据导入模板_{project_id}_{description}.xlsx"'
    
    return response


@login_required
@require_permission('can_manage_samples')
def import_template_list(request):
    """导入模板列表页面"""
    templates = ImportTemplate.objects.all().order_by('-created_at')
    return render(request, 'core/import_template_list.html', {
        'templates': templates
    })


@login_required
@require_permission('can_manage_samples')
def import_template_create(request):
    """创建导入模板"""
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        sample_type_description_id = request.POST.get('sample_type_description')
        is_active = request.POST.get('is_active') == 'on'
        
        # 处理文件上传
        template_file = request.FILES.get('template_file')
        
        if not name or not template_file:
            messages.error(request, '请填写模板名称并上传模板文件')
            return redirect('import_template_create')
        
        # 创建模板对象
        template = ImportTemplate(
            name=name,
            description=description,
            is_active=is_active,
            created_by=request.user
        )
        
        if sample_type_description_id:
            try:
                template.sample_type_description = SampleTypeDescription.objects.get(pk=sample_type_description_id)
            except SampleTypeDescription.DoesNotExist:
                pass
        
        # 保存文件
        fs = FileSystemStorage()
        filename = fs.save(template_file.name, template_file)
        template.template_file = filename
        template.save()
        
        messages.success(request, '模板创建成功')
        return redirect('import_template_list')
    
    # GET请求，显示表单
    sample_type_descriptions = SampleTypeDescription.objects.all()
    return render(request, 'core/import_template_form.html', {
        'sample_type_descriptions': sample_type_descriptions,
        'template': None
    })


@login_required
@require_permission('can_manage_samples')
def import_template_edit(request, template_id):
    """编辑导入模板"""
    template = get_object_or_404(ImportTemplate, pk=template_id)
    
    if request.method == 'POST':
        template.name = request.POST.get('name')
        template.description = request.POST.get('description', '')
        sample_type_description_id = request.POST.get('sample_type_description')
        template.is_active = request.POST.get('is_active') == 'on'
        
        # 处理文件上传（可选）
        template_file = request.FILES.get('template_file')
        if template_file:
            # 删除旧文件
            if template.template_file:
                fs = FileSystemStorage()
                if fs.exists(template.template_file.name):
                    fs.delete(template.template_file.name)
            # 保存新文件
            fs = FileSystemStorage()
            filename = fs.save(template_file.name, template_file)
            template.template_file = filename
        
        if sample_type_description_id:
            try:
                template.sample_type_description = SampleTypeDescription.objects.get(pk=sample_type_description_id)
            except SampleTypeDescription.DoesNotExist:
                template.sample_type_description = None
        else:
            template.sample_type_description = None
        
        template.save()
        
        messages.success(request, '模板更新成功')
        return redirect('import_template_list')
    
    # GET请求，显示表单
    sample_type_descriptions = SampleTypeDescription.objects.all()
    return render(request, 'core/import_template_form.html', {
        'sample_type_descriptions': sample_type_descriptions,
        'template': template
    })


@login_required
@require_permission('can_manage_samples')
def import_template_delete(request, template_id):
    """删除导入模板"""
    template = get_object_or_404(ImportTemplate, pk=template_id)
    
    if request.method == 'POST':
        # 删除文件
        if template.template_file:
            fs = FileSystemStorage()
            if fs.exists(template.template_file.name):
                fs.delete(template.template_file.name)
        template.delete()
        messages.success(request, '模板删除成功')
        return redirect('import_template_list')
    
    return render(request, 'core/import_template_confirm_delete.html', {
        'template': template
    })


@login_required
@require_permission('can_manage_samples')
def import_template_download(request, template_id):
    """下载导入模板"""
    template = get_object_or_404(ImportTemplate, pk=template_id)
    
    if template.template_file:
        fs = FileSystemStorage()
        file_path = template.template_file.path
        
        if fs.exists(template.template_file.name):
            with open(file_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = f'attachment; filename="{template.name}.xlsx"'
                return response
    
    messages.error(request, '模板文件不存在')
    return redirect('import_template_list')
