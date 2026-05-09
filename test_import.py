import pandas as pd
import os

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'senaite_lims.settings')
import django
django.setup()

from core.models import Project_Order, Sample, Test

# 读取Excel文件
file_path = r'D:\秦州_部门\孟令飞_LIMS\senaite.lims\senaite_lims\导入资料\下载 (3).xlsx'

# 读取测量记录工作表
xls = pd.ExcelFile(file_path)
temp_df_raw = pd.read_excel(xls, sheet_name='测量记录', header=None)

# 查找表头行
header_row_index = -1
for i in range(min(5, len(temp_df_raw))):
    if '序号' in str(temp_df_raw.iloc[i, 0]):
        header_row_index = i
        break

print(f'表头行索引: {header_row_index}')

if header_row_index >= 0:
    new_header = temp_df_raw.iloc[header_row_index]
    df = temp_df_raw[header_row_index+1:]
    df.columns = new_header
    
    # 测试get_value函数的逻辑
    def get_value(row, col_name):
        for col in df.columns:
            if col_name in str(col) or (col_name.replace(' ', '') in str(col).replace(' ', '')):
                return str(row[col]).strip() if pd.notna(row[col]) else ''
        return ''
    
    # 测试第一行数据
    first_row = df.iloc[0]
    print('\n第一行数据测试:')
    print(f'序号: {get_value(first_row, "序号")}')
    print(f'点位描述: {get_value(first_row, "点位描述")}')
    print(f'经度: {get_value(first_row, "经度")}')
    print(f'纬度: {get_value(first_row, "纬度")}')
    print(f'高程: {get_value(first_row, "高程")}')
    print(f'仪器示值Rγ(1): {get_value(first_row, "仪器示值Rγ(1)")}')
    print(f'平均值: {get_value(first_row, "平均值")}')
    
    # 查看有多少行数据
    print(f'\n总行数: {len(df)}')
    
    # 查看所有列名
    print('\n所有列名:')
    for col in df.columns:
        print(f'  {col}')
