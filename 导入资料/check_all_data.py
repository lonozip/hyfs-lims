#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
检查Excel文件中所有数据结构
"""

import pandas as pd

def check_excel_data(file_path):
    """检查Excel文件的完整结构"""
    try:
        xls = pd.ExcelFile(file_path)
        sheet_names = xls.sheet_names
        
        print(f"文件: {file_path}")
        print(f"工作表: {sheet_names}")
        print()
        
        for sheet_name in sheet_names:
            print(f"=== 工作表: {sheet_name} ===")
            df = pd.read_excel(xls, sheet_name=sheet_name, header=None)
            print(f"行数: {len(df)}, 列数: {len(df.columns)}")
            print()
            
            # 打印关键行
            for i in range(min(30, len(df))):
                row = df.iloc[i]
                print(f"第{i+1}行: {[str(x)[:20] for x in row.dropna().values]}")
            print()
            
    except Exception as e:
        print(f"读取文件失败: {str(e)}")

if __name__ == "__main__":
    file_path = r'D:\秦州_部门\孟令飞_LIMS\senaite.lims\senaite_lims\导入资料\下载 (3).xlsx'
    check_excel_data(file_path)
