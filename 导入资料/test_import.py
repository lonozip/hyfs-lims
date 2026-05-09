#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试导入功能，验证基本信息是否正确读取和保存
"""

import pandas as pd
from io import BytesIO

def test_read_basic_info(file_path):
    """测试读取基本信息"""
    try:
        xls = pd.ExcelFile(file_path)
        
        if '基本信息' in xls.sheet_names:
            basic_info_df = pd.read_excel(xls, sheet_name='基本信息', header=None)
            basic_info = {}
            
            # 解析基本信息（项目名称、监测日期等）
            for i in range(len(basic_info_df)):
                row = basic_info_df.iloc[i]
                if len(row) >= 2:
                    key = str(row[0]).strip()
                    value = str(row[1]).strip() if pd.notna(row[1]) else ''
                    if key and key != 'nan' and value and value != 'nan':
                        # 匹配基本信息字段
                        if '项目名称' in key:
                            basic_info['radiation_project_name'] = value
                        elif '监测日期' in key:
                            basic_info['radiation_monitoring_date'] = value
                        elif '监测地点' in key:
                            basic_info['radiation_location'] = value
                        elif '天气状况' in key:
                            basic_info['radiation_weather'] = value
                        elif '监测依据' in key:
                            basic_info['radiation_basis'] = value
                        elif '温度' in key:
                            basic_info['radiation_temperature'] = value
                        elif '湿度' in key:
                            basic_info['radiation_humidity'] = value
                        elif '测量工况' in key:
                            basic_info['radiation_conditions'] = value
            
            print("=== 解析到的基本信息 ===")
            for k, v in basic_info.items():
                print(f"  {k}: '{v}'")
            
            if not basic_info:
                print("警告：没有解析到任何基本信息！")
                return False
            return True
        else:
            print("错误：未找到'基本信息'工作表")
            return False
            
    except Exception as e:
        print(f"读取文件失败: {str(e)}")
        return False

if __name__ == "__main__":
    file_path = r'D:\秦州_部门\孟令飞_LIMS\senaite.lims\senaite_lims\导入资料\下载 (3).xlsx'
    test_read_basic_info(file_path)
