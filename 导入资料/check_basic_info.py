#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
检查Excel文件中基本信息工作表的具体结构
"""

import pandas as pd

def check_basic_info(file_path):
    """检查基本信息工作表的结构"""
    try:
        xls = pd.ExcelFile(file_path)
        
        if '基本信息' in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name='基本信息', header=None)
            
            print("=== 基本信息工作表内容 ===")
            print(f"行数: {len(df)}, 列数: {len(df.columns)}")
            print()
            
            # 打印前20行的详细内容
            print("前20行数据:")
            for i in range(min(20, len(df))):
                row = df.iloc[i]
                print(f"第{i+1}行: {[str(x)[:30] for x in row.dropna().values]}")
            
            print()
            print("=== 完整数据 ===")
            # 遍历所有行，查找键值对
            for i in range(len(df)):
                row = df.iloc[i]
                if len(row) >= 2:
                    key = str(row[0]).strip()
                    if key and key != 'nan':
                        values = []
                        for j in range(1, len(row)):
                            val = str(row[j]).strip()
                            if val and val != 'nan':
                                values.append(val)
                        if values:
                            print(f"  '{key}': '{', '.join(values)}'")
        else:
            print("未找到'基本信息'工作表")
            
    except Exception as e:
        print(f"读取文件失败: {str(e)}")

if __name__ == "__main__":
    file_path = r'D:\秦州_部门\孟令飞_LIMS\senaite.lims\senaite_lims\导入资料\下载 (3).xlsx'
    check_basic_info(file_path)
