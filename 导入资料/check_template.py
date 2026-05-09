#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
检查模板文件的数据
"""

import pandas as pd

def check_template_data(file_path):
    """检查模板文件的数据"""
    try:
        xls = pd.ExcelFile(file_path)
        sheet_names = xls.sheet_names
        
        print(f"文件: {file_path}")
        print(f"工作表: {sheet_names}")
        print()
        
        if '基本信息' in sheet_names:
            basic_info_df = pd.read_excel(xls, sheet_name='基本信息', header=None)
            
            print("=== 基本信息工作表 ===")
            print(f"总行数: {len(basic_info_df)}")
            print()
            
            # 查找宇宙射线信息区域
            print("=== 宇宙射线信息区域 ===")
            in_cosmic_ray = False
            cosmic_count = 0
            cosmic_data_rows = 0
            
            for i in range(len(basic_info_df)):
                row = basic_info_df.iloc[i]
                
                if '宇宙射线信息' in str(row[0]):
                    in_cosmic_ray = True
                    print(f"第{i+1}行: 宇宙射线信息标题")
                    continue
                
                if in_cosmic_ray:
                    if pd.isna(row[0]) or str(row[0]).strip() == '':
                        print(f"第{i+1}行: 空行，结束")
                        break
                    
                    if cosmic_count == 0:
                        print(f"第{i+1}行: 表头 = {[str(x)[:15] for x in row.dropna().values]}")
                    else:
                        # 检查是否有非空数据（除编号外）
                        has_data = False
                        for j in range(1, len(row)):
                            if pd.notna(row[j]) and str(row[j]).strip() != '':
                                has_data = True
                                break
                        if has_data:
                            cosmic_data_rows += 1
                            if cosmic_data_rows <= 5:
                                print(f"第{i+1}行: 有数据")
                    
                    cosmic_count += 1
            
            print(f"宇宙射线区域共{cosmic_count}行（含表头），有数据的行: {cosmic_data_rows}")
            print()
            
            # 查找仪器信息区域
            print("=== 仪器信息区域 ===")
            in_instrument = False
            instrument_count = 0
            instrument_data_rows = 0
            
            for i in range(len(basic_info_df)):
                row = basic_info_df.iloc[i]
                
                if '仪器信息' in str(row[0]):
                    in_instrument = True
                    print(f"第{i+1}行: 仪器信息标题")
                    continue
                
                if in_instrument:
                    if pd.isna(row[0]) or str(row[0]).strip() == '':
                        print(f"第{i+1}行: 空行，结束")
                        break
                    
                    if instrument_count == 0:
                        print(f"第{i+1}行: 表头 = {[str(x)[:15] for x in row.dropna().values]}")
                    else:
                        # 检查是否有非空数据（除编号外）
                        has_data = False
                        for j in range(1, len(row)):
                            if pd.notna(row[j]) and str(row[j]).strip() != '':
                                has_data = True
                                break
                        if has_data:
                            instrument_data_rows += 1
                            if instrument_data_rows <= 5:
                                print(f"第{i+1}行: 有数据")
                    
                    instrument_count += 1
            
            print(f"仪器信息区域共{instrument_count}行（含表头），有数据的行: {instrument_data_rows}")
            
    except Exception as e:
        print(f"读取文件失败: {str(e)}")

if __name__ == "__main__":
    print("=== 检查下载 (3).xlsx ===")
    check_template_data(r'D:\秦州_部门\孟令飞_LIMS\senaite.lims\senaite_lims\导入资料\下载 (3).xlsx')
    
    print("\n" + "="*50 + "\n")
    
    print("=== 检查环境γ辐射剂量率测量记录表.xlsx ===")
    check_template_data(r'D:\秦州_部门\孟令飞_LIMS\senaite.lims\senaite_lims\导入资料\环境γ辐射剂量率测量记录表.xlsx')
