from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import StandardLibrary, Standard, Standard_radiation_hygiene


@login_required
def standard_library_list(request):
    """标准库列表视图"""
    libraries = StandardLibrary.objects.all()
    return render(request, 'standard/library_list.html', {'libraries': libraries})


@login_required
def standard_library_detail(request, pk):
    """标准库详情视图"""
    library = get_object_or_404(StandardLibrary, pk=pk)
    standards = Standard.objects.filter(library=library)
    return render(request, 'standard/library_detail.html', {
        'library': library,
        'standards': standards
    })


@login_required
def standard_list(request):
    """标准列表视图函数"""
    standards = Standard.objects.all()
    return render(request, 'standard/standard_list.html', {'standards': standards})


@login_required
def standard_detail(request, pk):
    """标准详情视图"""
    standard = get_object_or_404(Standard, pk=pk)
    return render(request, 'standard/standard_detail.html', {'standard': standard})


@login_required
def standard_create(request):
    """添加标准视图函数"""
    # 获取所有标准库
    libraries = StandardLibrary.objects.all()
    
    if request.method == 'POST':
        # 获取表单数据
        library_id = request.POST.get('library')
        name = request.POST['name']
        test_name = request.POST['test_name']
        description = request.POST.get('description', '')
        unit = request.POST['unit']
        acceptance_reference_range = request.POST['acceptance_reference_range']
        standard_type = request.POST['standard_type']
        standard_id = request.POST['standard_id']
        collection_date = request.POST['collection_date']
        status = request.POST['status']
        
        # 获取标准库对象（可为空）
        library = None
        if library_id:
            library = StandardLibrary.objects.get(pk=library_id)
        
        # 创建标准对象
        standard = Standard(
            library=library,
            name=name,
            test_name=test_name,
            description=description,
            unit=unit,
            acceptance_reference_range=acceptance_reference_range,
            standard_type=standard_type,
            standard_id=standard_id,
            collection_date=collection_date,
            status=status,
            created_by=request.user
        )
        standard.save()
        
        # 显示成功消息
        from django.contrib import messages
        messages.success(request, '标准添加成功！')
        # 重定向到标准列表页面
        return render(request, 'standard/standard_list.html', {'standards': Standard.objects.all()})
    
    # 渲染添加标准模板
    return render(request, 'standard/standard_create.html', {'libraries': libraries})


@login_required
def standard_edit(request, pk):
    """编辑标准视图函数"""
    # 获取指定ID的标准，不存在则返回404
    standard = get_object_or_404(Standard, pk=pk)
    # 获取所有标准库
    libraries = StandardLibrary.objects.all()
    
    if request.method == 'POST':
        # 获取表单数据
        library_id = request.POST.get('library')
        name = request.POST['name']
        test_name = request.POST['test_name']
        description = request.POST.get('description', '')
        unit = request.POST['unit']
        acceptance_reference_range = request.POST['acceptance_reference_range']
        standard_type = request.POST['standard_type']
        standard_id = request.POST['standard_id']
        collection_date = request.POST['collection_date']
        status = request.POST['status']
        
        # 获取标准库对象（可为空）
        library = None
        if library_id:
            library = StandardLibrary.objects.get(pk=library_id)
        
        # 更新标准对象
        standard.library = library
        standard.name = name
        standard.test_name = test_name
        standard.description = description
        standard.unit = unit
        standard.acceptance_reference_range = acceptance_reference_range
        standard.standard_type = standard_type
        standard.standard_id = standard_id
        standard.collection_date = collection_date
        standard.status = status
        standard.save()
        
        # 显示成功消息
        from django.contrib import messages
        messages.success(request, '标准更新成功！')
        # 重定向到标准列表页面
        return render(request, 'standard/standard_list.html', {'standards': Standard.objects.all()})
    
    # 渲染编辑标准模板
    return render(request, 'standard/standard_edit.html', {'standard': standard, 'libraries': libraries})
