#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
扩展Excel表格中的宇宙射线信息和仪器信息行数，使其可以无限延伸
"""

import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.utils import get_column_letter

def extend_excel_tables():
    """扩展Excel表格中的宇宙射线信息和仪器信息表格"""
    
    # 读取现有Excel文件
    input_path = r'D:\秦州_部门\孟令飞_LIMS\senaite.lims\senaite_lims\导入资料\环境γ辐射剂量率测量记录表.xlsx'
    wb = openpyxl.load_workbook(input_path)
    
    # 获取基本信息工作表
    ws = wb['基本信息']
    
    # 设置样式
    normal_font = Font(size=11)
    center_alignment = Alignment(horizontal="center", vertical="center")
    thin_border = Border(left=Side(style='thin'), 
                         right=Side(style='thin'), 
                         top=Side(style='thin'), 
                         bottom=Side(style='thin'))
    
    # 定义扩展行数
    extend_rows = 47  # 添加47行，使总共有50行（原有3行 + 添加47行）
    
    # ========== 扩展宇宙射线信息表格 ==========
    # 宇宙射线信息表头在第15行，数据从第16行开始，原有3行数据在16-18行
    # 在第18行后面插入新行
    for i in range(extend_rows):
        new_row = 19 + i
        ws.insert_rows(new_row)
        
        # 设置编号
        ws[f'A{new_row}'] = i + 4  # 编号从4开始
        ws[f'A{new_row}'].font = normal_font
        ws[f'A{new_row}'].alignment = center_alignment
        ws[f'A{new_row}'].border = thin_border
        
        # 设置其他列的空单元格
        for col in range(2, 7):
            ws[f'{get_column_letter(col)}{new_row}'] = ""
            ws[f'{get_column_letter(col)}{new_row}'].font = normal_font
            ws[f'{get_column_letter(col)}{new_row}'].alignment = center_alignment
            ws[f'{get_column_letter(col)}{new_row}'].border = thin_border
        
        ws.row_dimensions[new_row].height = 20
    
    # ========== 扩展仪器信息表格 ==========
    # 仪器信息表头现在在第15 + extend_rows + 6 = 68行（因为宇宙射线信息增加了47行）
    # 原有仪器信息数据在第22-24行，现在向后移动到了第22+extend_rows行开始
    # 数据结束行现在是 24 + extend_rows = 71行
    # 在第71行后面插入新行
    
    for i in range(extend_rows):
        new_row = 72 + i
        ws.insert_rows(new_row)
        
        # 设置编号
        ws[f'A{new_row}'] = i + 4  # 编号从4开始
        ws[f'A{new_row}'].font = normal_font
        ws[f'A{new_row}'].alignment = center_alignment
        ws[f'A{new_row}'].border = thin_border
        
        # 设置其他列的空单元格
        for col in range(2, 7):
            ws[f'{get_column_letter(col)}{new_row}'] = ""
            ws[f'{get_column_letter(col)}{new_row}'].font = normal_font
            ws[f'{get_column_letter(col)}{new_row}'].alignment = center_alignment
            ws[f'{get_column_letter(col)}{new_row}'].border = thin_border
        
        ws.row_dimensions[new_row].height = 20
    
    # 保存修改后的文件
    output_path = r'D:\秦州_部门\孟令飞_LIMS\senaite.lims\senaite_lims\导入资料\环境γ辐射剂量率测量记录表.xlsx'
    wb.save(output_path)
    print(f"Excel文件已更新：{output_path}")
    print(f"宇宙射线信息表格：{3 + extend_rows}行")
    print(f"仪器信息表格：{3 + extend_rows}行")

if __name__ == "__main__":
    extend_excel_tables()
