# SENAITE LIMS - 环境γ辐射剂量率测量系统

## 项目简介

本系统是一个基于 Django 的环境γ辐射剂量率测量数据管理系统，用于管理和处理环境辐射监测数据。

## 主要功能

- **样品管理**：样品的录入、编辑、查询
- **测试管理**：测试记录的创建、导入、查询
- **Excel批量导入**：支持辐射剂量率数据的批量导入
- **自动计算**：自动计算平均值、标准差、宇宙射线响应值和环境γ辐射剂量率

## 技术栈

- Python 3.13+
- Django 6.0+
- pandas（Excel处理）
- weasyprint（PDF生成）

## 项目结构

```
senaite_lims/
├── core/                  # 核心应用
│   ├── models.py          # 数据模型（Sample, Test, Project_Order等）
│   ├── views.py           # 视图函数
│   ├── decorators.py      # 装饰器
│   └── migrations/        # 数据库迁移文件
├── Calculation/           # 计算模块
│   ├── __init__.py
│   ├── cosmicRayResponseCalculation.py  # 宇宙射线响应值计算
│   └── ...
├── standard/              # 标准数据应用
└── templates/             # HTML模板
```

## 计算模块说明

### cosmicRayResponseCalculation.py

提供环境γ辐射剂量率测量的核心计算功能：

| 函数名 | 功能 |
|:--|:--|
| `cosmicRayResponseCalculation()` | 计算宇宙射线响应值 |
| `calculate_r_gamma_avg_std()` | 计算平均值和标准差 |
| `calculate_env_gamma()` | 计算环境γ辐射剂量率 |

### 计算公式

环境γ辐射剂量率计算公式：
```
D = (Rγ × k1 / k2) - (Xc × k3)
```

参数说明：
- Rγ：仪器示值平均值
- k1：仪器校准/检定因子
- k2：仪器检验源效率因子
- Xc：宇宙射线响应值
- k3：屏蔽修正因子（楼房=0.8，平房=0.9，原野=1.0）

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 数据库迁移

```bash
python manage.py migrate
```

### 启动开发服务器

```bash
python manage.py runserver
```

### 访问系统

打开浏览器访问：http://127.0.0.1:8000/

## 使用说明

### Excel导入格式

辐射剂量率数据导入需要Excel文件包含：
1. **测量记录**工作表：包含点位描述、经纬度、高程、仪器示值等
2. **基本信息**工作表（可选）：包含项目名称、监测日期、宇宙射线信息、仪器信息等

### 必需列名

| 列名 | 说明 |
|:--|:--|
| 点位描述 | 测量地点描述 |
| 经度（E） | 经度值 |
| 纬度（N） | 纬度值 |
| 高程（H） | 高程值（米） |
| 仪器示值Rγ(1~5) | 5次仪器测量值 |
| 宇宙射线 | 宇宙射线响应值 |
| k3 | 屏蔽修正因子 |

## 许可证

MIT License
