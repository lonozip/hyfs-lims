# 核与辐射安全技术 LIMS 系统

一个基于Django 6.0开发的实验室信息管理系统(LIMS)，专为核与辐射安全技术领域设计。

## 项目简介

本系统提供完整的实验室管理功能，包括：
- 客户管理
- 样品管理
- 订单管理
- 测试管理
- 报告管理
- 员工管理
- 标准管理
- 部门管理

## 系统要求

- Python 3.13.0 或更高版本
- Django 6.0 或更高版本
- SQLite3 数据库（默认）

## 快速开始

### 1. 环境准备

#### Windows系统

```powershell
# 克隆或下载项目到本地
cd d:\秦州_部门\孟令飞_LIMS\senaite.lims\senaite_lims

# 创建虚拟环境（推荐）
python -m venv venv

# 激活虚拟环境
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

#### Linux/Mac系统

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 数据库初始化

```bash
# 执行数据库迁移
python manage.py migrate

# 创建超级管理员（可选）
python manage.py createsuperuser
```

### 3. 启动开发服务器

```bash
# 启动Django开发服务器
python manage.py runserver
```

服务器将在 `http://127.0.0.1:8000/` 启动

### 4. 访问系统

- **前台页面**: http://127.0.0.1:8000/
- **管理后台**: http://127.0.0.1:8000/admin/
- **注册页面**: http://127.0.0.1:8000/register/
- **登录页面**: http://127.0.0.1:8000/login/

## 系统功能

### 用户管理
- 用户注册和登录
- 基于角色的权限控制
- 管理员后台管理

### 客户管理
- 客户信息录入
- 客户列表查看
- 客户信息编辑和删除

### 样品管理
- 样品信息录入
- 样品状态跟踪（待处理、处理中、已完成、已取消）
- 样品与客户、订单关联
- 自动生成样品编号

### 订单管理
- 订单创建和管理
- 订单状态跟踪
- 订单与客户关联
- 自动生成订单编号

### 测试管理
- 测试记录管理
- 测试状态跟踪
- 测试结果录入
- 分析人员和验证人员管理

### 报告管理
- 报告创建和编辑
- 报告审核流程（编制→审核→签发）
- 报告状态管理
- 报告与方案、样品、标准关联
- 权限控制（审核、签发、拒绝）

### 员工管理
- 员工信息管理
- 部门分类
- 自动生成员工编号

### 标准管理
- 标准信息管理
- 测试类型管理
- 标准状态跟踪

### 数据可视化
- 首页数据统计
- 样品状态分布图表
- 订单状态分布图表
- 报告状态分布图表

## 项目结构

```
senaite_lims/
├── core/                          # 核心应用
│   ├── migrations/                # 数据库迁移文件
│   ├── static/                    # 静态文件
│   │   └── core/
│   │       └── admin/
│   │           └── js/
│   │               └── filter_orders.js
│   ├── templates/                 # 模板文件
│   │   └── core/
│   │       ├── base.html         # 基础模板
│   │       ├── home.html         # 首页
│   │       ├── login.html        # 登录页
│   │       ├── register.html     # 注册页
│   │       ├── client_list.html  # 客户列表
│   │       ├── sample_list.html  # 样品列表
│   │       ├── order_list.html   # 订单列表
│   │       ├── test_list.html    # 测试列表
│   │       ├── report.html       # 报告列表
│   │       ├── report_detail.html # 报告详情
│   │       ├── project_order.html # 方案列表
│   │       ├── project_order_detail.html # 方案详情
│   │       ├── standard.html     # 标准列表
│   │       ├── staff.html        # 员工列表
│   │       └── department.html   # 部门列表
│   ├── admin.py                  # 管理后台配置
│   ├── apps.py                   # 应用配置
│   ├── models.py                 # 数据模型
│   ├── urls.py                   # URL路由
│   ├── views.py                  # 视图函数
│   └── tests.py                  # 测试文件
├── static/                       # 全局静态文件
│   ├── css/                      # Bootstrap CSS
│   └── js/                       # Bootstrap JS
├── senaite_lims/                 # 项目配置
│   ├── settings.py               # 项目设置
│   ├── urls.py                   # 主URL配置
│   ├── wsgi.py                   # WSGI配置
│   └── asgi.py                   # ASGI配置
├── manage.py                     # Django管理脚本
├── requirements.txt              # 项目依赖
├── .gitignore                    # Git忽略文件
└── README.md                     # 项目说明文档
```

## 数据库模型

### 主要模型
- **Client**: 客户信息
- **Sample**: 样品信息
- **Order**: 订单信息
- **Test**: 测试记录
- **Standard**: 标准信息
- **Report**: 报告信息
- **Staff**: 员工信息
- **Department**: 部门信息
- **Project_Order**: 方案信息
- **Instrument**: 仪器设备信息

## 权限系统

### 报告权限
- `can_approve_report`: 可以审核报告
- `can_sign_report`: 可以签发报告
- `can_reject_report`: 可以拒绝报告

### 用户角色
- **普通用户**: 可以查看和管理基础数据
- **管理员**: 拥有所有权限，可以访问管理后台
- **审核人员**: 可以审核、签发和拒绝报告

## 配置说明

### 数据库配置

默认使用SQLite数据库，配置文件位于 `senaite_lims/settings.py`:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```

如需使用MySQL或PostgreSQL，请修改配置：

```python
# MySQL配置示例
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "your_database_name",
        "USER": "your_username",
        "PASSWORD": "your_password",
        "HOST": "localhost",
        "PORT": "3306",
    }
}
```

### 静态文件配置

```python
STATIC_URL = "static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATIC_ROOT = BASE_DIR / "collected_static"
```

### 时区设置

```python
TIME_ZONE = "UTC"
```

如需使用中国时区，修改为：
```python
TIME_ZONE = "Asia/Shanghai"
```

## 常见问题

### 1. 迁移失败

```bash
# 删除数据库文件
rm db.sqlite3

# 删除迁移文件
find core/migrations -name "*.py" -not -name "__init__.py" -delete

# 重新执行迁移
python manage.py makemigrations
python manage.py migrate
```

### 2. 静态文件无法加载

```bash
# 收集静态文件
python manage.py collectstatic
```

### 3. 端口被占用

```bash
# 使用其他端口启动
python manage.py runserver 8001
```

## 开发说明

### 添加新功能

1. 在 `core/models.py` 中定义数据模型
2. 执行 `python manage.py makemigrations` 生成迁移文件
3. 执行 `python manage.py migrate` 应用迁移
4. 在 `core/views.py` 中编写视图函数
5. 在 `core/urls.py` 中配置URL路由
6. 在 `core/templates/core/` 中创建模板文件

### 运行测试

```bash
python manage.py test
```

### 创建超级管理员

```bash
python manage.py createsuperuser
```

按照提示输入用户名、邮箱和密码。

## 技术栈

- **后端框架**: Django 6.0
- **前端框架**: Bootstrap 5
- **数据库**: SQLite3
- **Python版本**: 3.13.0

## 许可证

本项目仅供学习和研究使用。

## 联系方式

如有问题或建议，请联系项目维护者。

## 更新日志

### v1.0.0 (2026-01-29)
- 初始版本发布
- 实现基础LIMS功能
- 支持客户、样品、订单、测试、报告管理
- 实现用户认证和权限控制
- 添加数据可视化功能