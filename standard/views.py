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
