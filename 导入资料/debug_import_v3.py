#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
调试导入功能，验证修复后的数据解析
"""

import pandas as pd

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
            
            in_cosmic_ray_section = False
            in_instrument_section = False
            cosmic_ray_header = None
            instrument_header = None
            cosmic_ray_info = []
            instrument_info = []
            
            for i in range(len(basic_info_df)):
                row = basic_info_df.iloc[i]
                
                # 检测宇宙射线信息区域
                if '宇宙射线信息' in str(row[0]):
                    in_cosmic_ray_section = True
                    in_instrument_section = False
                    continue
                
                # 检测仪器信息区域
                if '仪器信息' in str(row[0]):
                    in_instrument_section = True
                    in_cosmic_ray_section = False
                    continue
                
                # 检测空行，结束当前区域
                if pd.isna(row[0]) or str(row[0]).strip() == '':
                    if in_cosmic_ray_section and cosmic_ray_header:
                        in_cosmic_ray_section = False
                    if in_instrument_section and instrument_header:
                        in_instrument_section = False
                    continue
                
                # 处理宇宙射线信息
                elif in_cosmic_ray_section:
                    if cosmic_ray_header is None:
                        cosmic_ray_header = [str(x).strip() for x in row.dropna().values]
                    else:
                        # 读取数据行，转换为前端期望的字段名
                        item = {}
                        for j, col_name in enumerate(cosmic_ray_header):
                            if j < len(row):
                                value = str(row[j]).strip() if pd.notna(row[j]) else ''
                                # 转换字段名为前端期望的格式
                                if '测量地点' in col_name:
                                    item['location'] = value
                                elif '经度' in col_name:
                                    item['longitude'] = value
                                elif '纬度' in col_name:
                                    item['latitude'] = value
                                elif '高程' in col_name:
                                    item['elevation'] = value
                                elif '响应值' in col_name or 'Xc' in col_name:
                                    item['xc_response'] = value
                                elif col_name == '编号':
                                    item['id'] = value
                                else:
                                    item[col_name] = value
                        # 检查是否有除编号外的实际数据
                        if item.get('location') or item.get('longitude') or item.get('latitude') or item.get('elevation') or item.get('xc_response'):
                            cosmic_ray_info.append(item)
                
                # 处理仪器信息
                elif in_instrument_section:
                    if instrument_header is None:
                        instrument_header = [str(x).strip() for x in row.dropna().values]
                    else:
                        # 读取数据行，转换为前端期望的字段名
                        item = {}
                        for j, col_name in enumerate(instrument_header):
                            if j < len(row):
                                value = str(row[j]).strip() if pd.notna(row[j]) else ''
                                # 转换字段名为前端期望的格式
                                if '名称' in col_name:
                                    item['name'] = value
                                elif '型号' in col_name:
                                    item['model'] = value
                                elif '编号' in col_name:
                                    # 第二个编号字段作为code
                                    if 'code' not in item:
                                        item['id'] = value
                                    else:
                                        item['code'] = value
                                elif 'k1' in col_name or '校准' in col_name or '检定' in col_name:
                                    item['k1'] = value
                                elif 'k2' in col_name or '效率' in col_name:
                                    item['k2'] = value
                                else:
                                    item[col_name] = value
                        # 检查是否有除编号外的实际数据
                        if item.get('name') or item.get('model') or item.get('code') or item.get('k1') or item.get('k2'):
                            instrument_info.append(item)
            
            print("=== 解析结果 ===")
            print(f"宇宙射线信息条数: {len(cosmic_ray_info)}")
            if cosmic_ray_info:
                print(f"宇宙射线信息示例（前端格式）:")
                for item in cosmic_ray_info[:3]:
                    print(f"  {item}")
            print(f"仪器信息条数: {len(instrument_info)}")
            if instrument_info:
                print(f"仪器信息示例（前端格式）:")
                for item in instrument_info[:3]:
                    print(f"  {item}")
        
    except Exception as e:
        print(f"读取文件失败: {str(e)}")

if __name__ == "__main__":
    file_path = r'D:\秦州_部门\孟令飞_LIMS\senaite.lims\senaite_lims\导入资料\下载 (3).xlsx'
    debug_excel_import(file_path)
