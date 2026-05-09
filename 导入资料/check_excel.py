#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
检查Excel文件结构
"""

import pandas as pd

def check_excel_structure(file_path):
    """检查Excel文件的工作表和列"""
    try:
        xls = pd.ExcelFile(file_path)
        sheet_names = xls.sheet_names
        
        print(f"文件: {file_path}")
        print(f"工作表数量: {len(sheet_names)}")
        print(f"工作表名称: {sheet_names}")
        print()
        
        for sheet_name in sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name)
            print(f"工作表: {sheet_name}")
            print(f"行数: {len(df)}")
            print(f"列数: {len(df.columns)}")
            print(f"列名: {list(df.columns)}")
            print()
            
            # 显示前3行数据
            print("前3行数据:")
            print(df.head(3))
            print("-" * 50)
            print()
        
    except Exception as e:
        print(f"读取文件失败: {str(e)}")

if __name__ == "__main__":
    file_path = r'D:\秦州_部门\孟令飞_LIMS\senaite.lims\senaite_lims\导入资料\下载 (3).xlsx'
    check_excel_structure(file_path)
