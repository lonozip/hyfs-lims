# 核与辐射安全技术 LIMS 系统

核与辐射安全技术实验室信息管理系统（LIMS）是基于 Django 框架开发的专业实验室管理平台，用于管理实验室的客户、订单、方案、样品和报告等业务流程。

## 功能特性

### 核心功能模块

1. **客户管理**
   - 客户信息的增删改查
   - 客户搜索与筛选
   - 支持批量导入客户数据（自动去重）

2. **订单管理**
   - 订单创建与编辑
   - 订单状态跟踪
   - 关联客户信息

3. **方案管理**
   - 方案创建与编辑
   - 客户与订单联动选择（支持搜索）
   - 样品类型多选与描述选择
   - 样品描述数量设置
   - 标准关联管理
   - 员工分配管理
   - 方案完成自动生成报告

4. **样品管理**
   - 样品信息自动生成（根据方案配置）
   - 样品状态管理
   - 关联方案和订单信息
   - 样品搜索功能
   - 样品创建自动生成测试记录

5. **测试管理**
   - 测试记录管理
   - 样品类型描述关联
   - 地址信息录入
   - 测试照片上传（支持相机照片格式）
   - 测试照片缩略图展示
   - 测试搜索功能

6. **报告管理**
   - 报告自动生成（方案完成时）
   - PDF报告导出（美观紧凑格式）
   - 报告审核流程（编制→审核→签发）
   - 测试更新同步报告
   - 地址和照片缩略图展示

7. **标准管理**
   - 测试标准管理
   - 辐射卫生标准管理
   - 标准库管理

8. **组织管理**
   - 部门管理
   - 职位管理
   - 员工信息管理（含员工编号）

9. **员工账号管理**
   - 员工账号创建与管理
   - 系统权限控制（方案管理、样本管理、标准管理、组织架构、样品类型管理、样品类型描述、管理后台）
   - 初始密码统一设置

10. **首页仪表盘**
    - 测试状态分布图表
    - 数据统计概览

## 技术栈

- **框架**: Django 6.0
- **语言**: Python 3.13
- **前端**: Bootstrap 5, Select2, Chart.js
- **数据库**: SQLite（开发环境）/ PostgreSQL（生产环境）
- **PDF生成**: weasyprint

## 快速开始

### 环境要求

- Python 3.10+
- pip
- Git

### 安装步骤

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd senaite.lims/senaite_lims
   ```

2. **创建虚拟环境**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **数据库迁移**
   ```bash
   python manage.py migrate
   ```

5. **创建超级用户**
   ```bash
   python manage.py createsuperuser
   ```

6. **运行开发服务器**
   ```bash
   python manage.py runserver
   ```

7. **访问系统**
   - 访问 http://127.0.0.1:8000/
   - 使用超级用户账号登录

## 数据导入

系统提供了数据导入功能，可批量导入客户数据：

### 导入客户数据

将客户数据文件（Markdown格式）放置在 `导入资料/` 目录下，系统支持自动导入并去重。

## 项目结构

```
senaite_lims/
├── core/                    # 核心应用
│   ├── migrations/          # 数据库迁移文件
│   ├── templates/           # 模板文件
│   ├── static/              # 静态资源
│   ├── __init__.py
│   ├── admin.py             # 后台管理配置
│   ├── apps.py              # 应用配置
│   ├── models.py            # 数据模型
│   ├── views.py             # 视图函数
│   ├── urls.py              # 路由配置
│   └── decorators.py        # 自定义装饰器
├── standard/                # 标准管理应用
│   ├── migrations/
│   ├── templates/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── sample_type/             # 样品类型应用
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── senaite_lims/            # 项目配置
│   ├── __init__.py
│   ├── settings.py          # 项目配置
│   ├── urls.py              # 全局路由
│   ├── wsgi.py
│   └── asgi.py
├── static/                  # 全局静态资源
├── media/                   # 媒体文件（照片等）
├── report_pdfs/             # 生成的PDF报告
├── 导入资料/                 # 数据导入文件
├── manage.py                # Django管理命令
├── requirements.txt         # 依赖列表
└── README.md                # 项目说明
```

## 主要数据模型

| 模型 | 说明 |
|------|------|
| Client | 客户信息 |
| Order | 订单信息 |
| Project_Order | 方案信息 |
| Sample | 样品信息 |
| Test | 测试记录 |
| Report | 报告信息 |
| Staff | 员工信息 |
| Department | 部门信息 |
| Position | 职位信息 |
| SampleType | 样品类型 |
| SampleTypeDescription | 样品类型描述 |
| Standard | 测试标准 |
| Standard_radiation_hygiene | 辐射卫生标准 |

## 使用说明

### 添加方案流程

1. 登录系统后，点击"方案管理"
2. 点击"添加方案"按钮
3. 填写方案基本信息（名称、描述等）
4. 选择客户（支持搜索）
5. 根据客户选择关联的订单（支持搜索）
6. 选择样品类型（支持多选）
7. 为每个样品类型选择描述并设置数量
8. 选择关联标准
9. 分配负责员工
10. 点击"保存"完成创建（自动生成样品和测试记录）

### 测试管理流程

1. 在"测试管理"页面查看所有测试记录
2. 点击测试ID进入详情页
3. 填写测试结果、地址信息
4. 上传测试照片
5. 保存测试记录（自动同步更新报告）

### 生成报告流程

1. 方案创建时自动生成报告草稿
2. 在报告详情页面查看关联样品和测试
3. 提交审核→审核通过→签发报告
4. 可下载PDF版本

## 配置说明

### 数据库配置

在 `senaite_lims/settings.py` 中配置数据库：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### 媒体文件配置

```python
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'
```

## 许可证

本项目仅供内部使用。

## 联系方式

如有问题或建议，请联系系统管理员。
