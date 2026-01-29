# 导入Django应用配置模块
from django.apps import AppConfig


class CoreConfig(AppConfig):
    """核心应用配置类"""
    # 应用名称
    name = "core"
    # 应用的显示名称
    verbose_name = "核心应用"
