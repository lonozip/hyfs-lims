#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
调试仪器信息解析
"""

import pandas as pd

def debug_instrument_info(file_path):
    """调试仪器信息解析"""
    try:
        xls = pd.ExcelFile(file_path)
        sheet_names = xls.sheet_names
        
        if '基本信息' in sheet_names:
            basic_info_df = pd.read_excel(xls, sheet_name='基本信息', header=None)
            
            print("=== 基本信息工作表 - 查找仪器信息区域 ===")
            
            in_instrument_section = False
            instrument_header = None
            instrument_start_row = -1
            instrument_end_row = -1
            
            for i in range(len(basic_info_df)):
                row = basic_info_df.iloc[i]
                
                if '仪器信息' in str(row[0]):
                    in_instrument_section = True
                    instrument_start_row = i
                    print(f"第{i+1}行: 检测到仪器信息区域")
                    continue
                
                if in_instrument_section:
                    if instrument_header is None:
                        # 表头行
                        instrument_header = [str(x).strip() for x in row.dropna().values]
                        print(f"第{i+1}行: 表头 = {instrument_header}")
                    else:
                        # 检查是否是空行
                        if pd.isna(row[0]) or str(row[0]).strip() == '':
                            instrument_end_row = i
                            print(f"第{i+1}行: 空行，结束仪器信息区域")
                            break
                        else:
                            # 数据行
                            print(f"第{i+1}行: 数据 = {[str(x)[:20] for x in row.values]}")
            
            print(f"\n仪器信息区域: 第{instrument_start_row+1}行到第{instrument_end_row+1}行")
            
    except Exception as e:
        print(f"读取文件失败: {str(e)}")

if __name__ == "__main__":
    file_path = r'D:\秦州_部门\孟令飞_LIMS\senaite.lims\senaite_lims\导入资料\下载 (3).xlsx'
    debug_instrument_info(file_path)