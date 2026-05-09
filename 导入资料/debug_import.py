#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
调试导入功能，验证数据解析
"""

import pandas as pd
from io import BytesIO

def debug_excel_import(file_path):
    """调试Excel导入"""
    try:
        xls = pd.ExcelFile(file_path)
        sheet_names = xls.sheet_names
        
        print(f"文件: {file_path}")
        print(f"工作表: {sheet_names}")
        print()
        
        # 解析基本信息工作表
        if '基本信息' in sheet_names:
            basic_info_df = pd.read_excel(xls, sheet_name='基本信息', header=None)
            print("=== 基本信息工作表解析 ===")
            
            in_cosmic_ray_section = False
            in_instrument_section = False
            cosmic_ray_header = None
            instrument_header = None
            cosmic_ray_info = []
            instrument_info = []
            basic_info = {}
            
            for i in range(len(basic_info_df)):
                row = basic_info_df.iloc[i]
                
                # 检测宇宙射线信息区域
                if '宇宙射线信息' in str(row[0]):
                    in_cosmic_ray_section = True
                    in_instrument_section = False
                    print(f"第{i+1}行: 检测到宇宙射线信息区域")
                    continue
                
                # 检测仪器信息区域
                if '仪器信息' in str(row[0]):
                    in_instrument_section = True
                    in_cosmic_ray_section = False
                    print(f"第{i+1}行: 检测到仪器信息区域")
                    continue
                
                # 检测空行，结束当前区域
                if pd.isna(row[0]) or str(row[0]).strip() == '':
                    if in_cosmic_ray_section and cosmic_ray_header:
                        in_cosmic_ray_section = False
                        print(f"第{i+1}行: 结束宇宙射线区域")
                    if in_instrument_section and instrument_header:
                        in_instrument_section = False
                        print(f"第{i+1}行: 结束仪器信息区域")
                    continue
                
                # 处理基本信息
                if not in_cosmic_ray_section and not in_instrument_section:
                    if len(row) >= 2:
                        key = str(row[0]).strip()
                        value = str(row[1]).strip() if pd.notna(row[1]) else ''
                        if key and key != 'nan' and value and value != 'nan':
                            basic_info[key] = value
                            print(f"第{i+1}行: 基本信息 - {key} = {value}")
                
                # 处理宇宙射线信息
                elif in_cosmic_ray_section:
                    if cosmic_ray_header is None:
                        cosmic_ray_header = [str(x).strip() for x in row.dropna().values]
                        print(f"第{i+1}行: 宇宙射线表头 = {cosmic_ray_header}")
                    else:
                        item = {}
                        for j, col_name in enumerate(cosmic_ray_header):
                            if j < len(row):
                                item[col_name] = str(row[j]).strip() if pd.notna(row[j]) else ''
                        if any(item.values()):
                            cosmic_ray_info.append(item)
                            print(f"第{i+1}行: 宇宙射线数据 = {item}")
                
                # 处理仪器信息
                elif in_instrument_section:
                    if instrument_header is None:
                        instrument_header = [str(x).strip() for x in row.dropna().values]
                        print(f"第{i+1}行: 仪器信息表头 = {instrument_header}")
                    else:
                        item = {}
                        for j, col_name in enumerate(instrument_header):
                            if j < len(row):
                                item[col_name] = str(row[j]).strip() if pd.notna(row[j]) else ''
                        if any(item.values()):
                            instrument_info.append(item)
                            print(f"第{i+1}行: 仪器信息数据 = {item}")
            
            print()
            print("=== 解析结果 ===")
            print(f"基本信息: {basic_info}")
            print(f"宇宙射线信息条数: {len(cosmic_ray_info)}")
            if cosmic_ray_info:
                print(f"宇宙射线信息示例: {cosmic_ray_info[:3]}")
            print(f"仪器信息条数: {len(instrument_info)}")
            if instrument_info:
                print(f"仪器信息示例: {instrument_info[:3]}")
        
        # 解析测量记录工作表
        if '测量记录' in sheet_names:
            print()
            print("=== 测量记录工作表 ===")
            temp_df_raw = pd.read_excel(xls, sheet_name='测量记录', header=None)
            
            # 查找表头行
            header_row = -1
            for i in range(min(5, len(temp_df_raw))):
                if '序号' in str(temp_df_raw.iloc[i, 0]):
                    header_row = i
                    break
            
            if header_row >= 0:
                print(f"表头行: 第{header_row+1}行")
                new_header = temp_df_raw.iloc[header_row]
                df = temp_df_raw[header_row+1:]
                df.columns = new_header
                
                print(f"列名: {list(df.columns)}")
                print(f"数据行数: {len(df)}")
                
                # 显示前5行数据
                print("\n前5行数据:")
                for idx, row in df.head(5).iterrows():
                    print(f"  序号: {row['序号']}, 点位描述: {row['点位描述']}, 平均值: {row['平均值']}")
                    
    except Exception as e:
        print(f"读取文件失败: {str(e)}")

if __name__ == "__main__":
    file_path = r'D:\秦州_部门\孟令飞_LIMS\senaite.lims\senaite_lims\导入资料\下载 (3).xlsx'
    debug_excel_import(file_path)
