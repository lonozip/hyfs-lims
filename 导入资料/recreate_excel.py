#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
重新创建环境γ辐射剂量率测量记录表Excel模板，修复编号错误
"""

import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.workbook import Workbook

def create_excel_template():
    """创建环境γ辐射剂量率测量记录表Excel模板"""
    
    # 创建工作簿
    wb = Workbook()
    
    # 创建基本信息表
    create_basic_info_sheet(wb)
    
    # 创建测量记录表
    create_measurement_sheet(wb)
    
    # 创建计算说明表
    create_calc_sheet(wb)
    
    # 保存文件
    output_path = r'D:\秦州_部门\孟令飞_LIMS\senaite.lims\senaite_lims\导入资料\环境γ辐射剂量率测量记录表.xlsx'
    wb.save(output_path)
    print(f"Excel文件已创建：{output_path}")

def create_basic_info_sheet(wb):
    """创建基本信息工作表"""
    ws = wb.create_sheet(title="基本信息")
    
    # 设置字体样式
    title_font = Font(bold=True, size=14, color="FFFFFF")
    header_font = Font(bold=True, size=11, color="FFFFFF")
    label_font = Font(bold=True, size=11, color="276749")
    normal_font = Font(size=11)
    
    # 设置填充样式
    title_fill = PatternFill(start_color="1a365d", end_color="1a365d", fill_type="solid")
    header_fill = PatternFill(start_color="4a5568", end_color="4a5568", fill_type="solid")
    label_fill = PatternFill(start_color="f0fff4", end_color="f0fff4", fill_type="solid")
    
    # 设置对齐样式
    center_alignment = Alignment(horizontal="center", vertical="center")
    left_alignment = Alignment(horizontal="left", vertical="center")
    
    # 设置边框样式
    thin_border = Border(left=Side(style='thin'), 
                         right=Side(style='thin'), 
                         top=Side(style='thin'), 
                         bottom=Side(style='thin'))
    
    # 标题
    ws.merge_cells('A1:H1')
    ws['A1'] = "环境γ辐射剂量率测量记录表"
    ws['A1'].font = title_font
    ws['A1'].fill = title_fill
    ws['A1'].alignment = center_alignment
    ws.row_dimensions[1].height = 30
    
    # 使用说明
    ws.merge_cells('A2:H2')
    ws['A2'] = "使用说明：本模板用于一键导入环境γ辐射剂量率测量数据。请按表头字段填写对应数据后导入。"
    ws['A2'].font = Font(size=10, color="2c5282")
    ws['A2'].fill = PatternFill(start_color="ebf8ff", end_color="ebf8ff", fill_type="solid")
    ws.row_dimensions[2].height = 25
    
    # 基本信息标题
    ws.merge_cells('A4:H4')
    ws['A4'] = "一、基本信息"
    ws['A4'].font = Font(bold=True, size=12, color="2c5282")
    ws.row_dimensions[4].height = 25
    
    # 基本信息表格
    basic_info_labels = [
        "项目名称", "监测日期", "监测地点", "天气状况",
        "监测依据", "温度（℃）", "湿度（%）", "测量工况"
    ]
    
    for i, label in enumerate(basic_info_labels):
        row = 5 + i
        ws[f'A{row}'] = label
        ws[f'A{row}'].font = label_font
        ws[f'A{row}'].fill = label_fill
        ws[f'A{row}'].alignment = left_alignment
        ws[f'A{row}'].border = thin_border
        
        ws[f'B{row}'] = ""
        ws[f'B{row}'].font = normal_font
        ws[f'B{row}'].alignment = left_alignment
        ws[f'B{row}'].border = thin_border
        
        ws.merge_cells(f'B{row}:H{row}')
    
    for row in range(5, 13):
        ws.row_dimensions[row].height = 22
    
    # 宇宙射线信息标题
    ws.merge_cells('A14:H14')
    ws['A14'] = "宇宙射线信息"
    ws['A14'].font = Font(bold=True, size=11, color="3182ce")
    ws.row_dimensions[14].height = 22
    
    # 宇宙射线信息表头
    cosmic_headers = ["编号", "测量地点", "经度（E）", "纬度（N）", "高程（H）", "响应值Xc（Gy/h）"]
    for i, header in enumerate(cosmic_headers):
        col = i + 1
        ws[f'{get_column_letter(col)}15'] = header
        ws[f'{get_column_letter(col)}15'].font = header_font
        ws[f'{get_column_letter(col)}15'].fill = header_fill
        ws[f'{get_column_letter(col)}15'].alignment = center_alignment
        ws[f'{get_column_letter(col)}15'].border = thin_border
    
    # 宇宙射线信息数据行（50行）
    for row in range(16, 66):
        ws[f'A{row}'] = row - 15  # 编号从1开始，连续递增
        ws[f'A{row}'].font = normal_font
        ws[f'A{row}'].alignment = center_alignment
        ws[f'A{row}'].border = thin_border
        
        for col in range(2, 7):
            ws[f'{get_column_letter(col)}{row}'] = ""
            ws[f'{get_column_letter(col)}{row}'].font = normal_font
            ws[f'{get_column_letter(col)}{row}'].alignment = center_alignment
            ws[f'{get_column_letter(col)}{row}'].border = thin_border
        
        ws.row_dimensions[row].height = 20
    
    ws.row_dimensions[15].height = 22
    
    # 仪器信息标题
    ws.merge_cells('A67:H67')
    ws['A67'] = "仪器信息"
    ws['A67'].font = Font(bold=True, size=11, color="3182ce")
    ws.row_dimensions[67].height = 22
    
    # 仪器信息表头
    instrument_headers = ["编号", "名称", "型号", "编号", "校准/检定因子k1", "效率因子k2"]
    for i, header in enumerate(instrument_headers):
        col = i + 1
        ws[f'{get_column_letter(col)}68'] = header
        ws[f'{get_column_letter(col)}68'].font = header_font
        ws[f'{get_column_letter(col)}68'].fill = header_fill
        ws[f'{get_column_letter(col)}68'].alignment = center_alignment
        ws[f'{get_column_letter(col)}68'].border = thin_border
    
    # 仪器信息数据行（50行）
    for row in range(69, 119):
        ws[f'A{row}'] = row - 68  # 编号从1开始，连续递增
        ws[f'A{row}'].font = normal_font
        ws[f'A{row}'].alignment = center_alignment
        ws[f'A{row}'].border = thin_border
        
        for col in range(2, 7):
            ws[f'{get_column_letter(col)}{row}'] = ""
            ws[f'{get_column_letter(col)}{row}'].font = normal_font
            ws[f'{get_column_letter(col)}{row}'].alignment = center_alignment
            ws[f'{get_column_letter(col)}{row}'].border = thin_border
        
        ws.row_dimensions[row].height = 20
    
    ws.row_dimensions[68].height = 22
    
    # 设置列宽
    ws.column_dimensions['A'].width = 12
    ws.column_dimensions['B'].width = 20
    ws.column_dimensions['C'].width = 15
    ws.column_dimensions['D'].width = 15
    ws.column_dimensions['E'].width = 15
    ws.column_dimensions['F'].width = 20
    ws.column_dimensions['G'].width = 15
    ws.column_dimensions['H'].width = 15

def create_measurement_sheet(wb):
    """创建测量记录工作表"""
    ws = wb.create_sheet(title="测量记录")
    
    # 设置样式
    title_font = Font(bold=True, size=14, color="FFFFFF")
    header_font = Font(bold=True, size=10, color="FFFFFF")
    normal_font = Font(size=10)
    
    title_fill = PatternFill(start_color="1a365d", end_color="1a365d", fill_type="solid")
    header_fill = PatternFill(start_color="4a5568", end_color="4a5568", fill_type="solid")
    even_fill = PatternFill(start_color="f7fafc", end_color="f7fafc", fill_type="solid")
    
    center_alignment = Alignment(horizontal="center", vertical="center")
    left_alignment = Alignment(horizontal="left", vertical="center")
    
    thin_border = Border(left=Side(style='thin'), 
                         right=Side(style='thin'), 
                         top=Side(style='thin'), 
                         bottom=Side(style='thin'))
    
    # 标题
    ws.merge_cells('A1:T1')
    ws['A1'] = "二、测量记录"
    ws['A1'].font = title_font
    ws['A1'].fill = title_fill
    ws['A1'].alignment = center_alignment
    ws.row_dimensions[1].height = 30
    
    # 表头
    headers = [
        "序号", "点位描述", "经度（E）", "纬度（N）", "高程（H）",
        "仪器示值Rγ(1)", "仪器示值Rγ(2)", "仪器示值Rγ(3)", "仪器示值Rγ(4)", "仪器示值Rγ(5)",
        "仪器示值Rγ(6)", "仪器示值Rγ(7)", "仪器示值Rγ(8)", "仪器示值Rγ(9)", "仪器示值Rγ(10)",
        "宇宙射线", "k3", "平均值", "标准差", "备注"
    ]
    
    for i, header in enumerate(headers):
        col = i + 1
        ws[f'{get_column_letter(col)}2'] = header
        ws[f'{get_column_letter(col)}2'].font = header_font
        ws[f'{get_column_letter(col)}2'].fill = header_fill
        ws[f'{get_column_letter(col)}2'].alignment = center_alignment
        ws[f'{get_column_letter(col)}2'].border = thin_border
    
    # 数据行（24行）
    for row in range(3, 27):
        ws[f'A{row}'] = row - 2
        ws[f'A{row}'].font = normal_font
        ws[f'A{row}'].alignment = center_alignment
        ws[f'A{row}'].border = thin_border
        ws[f'A{row}'].fill = even_fill if (row - 2) % 2 == 0 else PatternFill(start_color="ffffff", end_color="ffffff", fill_type="solid")
        
        for col in range(2, 21):
            ws[f'{get_column_letter(col)}{row}'] = ""
            ws[f'{get_column_letter(col)}{row}'].font = normal_font
            ws[f'{get_column_letter(col)}{row}'].alignment = left_alignment if col == 2 else center_alignment
            ws[f'{get_column_letter(col)}{row}'].border = thin_border
            ws[f'{get_column_letter(col)}{row}'].fill = even_fill if (row - 2) % 2 == 0 else PatternFill(start_color="ffffff", end_color="ffffff", fill_type="solid")
    
    # 设置行高和列宽
    ws.row_dimensions[2].height = 22
    for row in range(3, 27):
        ws.row_dimensions[row].height = 18
    
    ws.column_dimensions['A'].width = 8
    ws.column_dimensions['B'].width = 15
    ws.column_dimensions['C'].width = 12
    ws.column_dimensions['D'].width = 12
    ws.column_dimensions['E'].width = 10
    ws.column_dimensions['F'].width = 14
    ws.column_dimensions['G'].width = 14
    ws.column_dimensions['H'].width = 14
    ws.column_dimensions['I'].width = 14
    ws.column_dimensions['J'].width = 14
    ws.column_dimensions['K'].width = 14
    ws.column_dimensions['L'].width = 14
    ws.column_dimensions['M'].width = 14
    ws.column_dimensions['N'].width = 14
    ws.column_dimensions['O'].width = 14
    ws.column_dimensions['P'].width = 12
    ws.column_dimensions['Q'].width = 6
    ws.column_dimensions['R'].width = 10
    ws.column_dimensions['S'].width = 10
    ws.column_dimensions['T'].width = 12

def create_calc_sheet(wb):
    """创建计算说明工作表"""
    ws = wb.create_sheet(title="计算说明")
    
    # 设置样式
    title_font = Font(bold=True, size=14, color="FFFFFF")
    section_font = Font(bold=True, size=12, color="2c5282")
    header_font = Font(bold=True, size=10, color="FFFFFF")
    normal_font = Font(size=11)
    
    title_fill = PatternFill(start_color="1a365d", end_color="1a365d", fill_type="solid")
    header_fill = PatternFill(start_color="4a5568", end_color="4a5568", fill_type="solid")
    formula_fill = PatternFill(start_color="fffaf0", end_color="fffaf0", fill_type="solid")
    
    center_alignment = Alignment(horizontal="center", vertical="center")
    left_alignment = Alignment(horizontal="left", vertical="center")
    
    thin_border = Border(left=Side(style='thin'), 
                         right=Side(style='thin'), 
                         top=Side(style='thin'), 
                         bottom=Side(style='thin'))
    
    # 标题
    ws.merge_cells('A1:D1')
    ws['A1'] = "三、计算说明"
    ws['A1'].font = title_font
    ws['A1'].fill = title_fill
    ws['A1'].alignment = center_alignment
    ws.row_dimensions[1].height = 30
    
    # 测值计算公式
    ws['A3'] = "①测值计算公式："
    ws['A3'].font = section_font
    ws.row_dimensions[3].height = 25
    
    ws.merge_cells('A4:D4')
    ws['A4'] = "D = (Rγ × k1 / k2) - (Xc × k3)"
    ws['A4'].font = Font(size=16, color="c2410c", bold=True)
    ws['A4'].fill = formula_fill
    ws['A4'].alignment = center_alignment
    ws.row_dimensions[4].height = 40
    
    # 参数说明表头
    param_headers = ["参数", "说明"]
    for i, header in enumerate(param_headers):
        col = i + 1
        ws[f'{get_column_letter(col)}6'] = header
        ws[f'{get_column_letter(col)}6'].font = header_font
        ws[f'{get_column_letter(col)}6'].fill = header_fill
        ws[f'{get_column_letter(col)}6'].alignment = center_alignment
        ws[f'{get_column_letter(col)}6'].border = thin_border
    
    # 参数说明数据
    params = [
        ["k1", "仪器检定/校准因子"],
        ["k2", "仪器检验源效率因子（如仪器无检验源，则该值取1）"],
        ["k3", "建筑物对宇宙射线的屏蔽修正因子（楼房取0.8，平房取0.9，原野/道路取1）"],
        ["Xc", "宇宙射线响应值（计算参考HJ 61-2021附录D）"]
    ]
    
    for i, (param, desc) in enumerate(params):
        row = 7 + i
        ws[f'A{row}'] = param
        ws[f'A{row}'].font = normal_font
        ws[f'A{row}'].alignment = center_alignment
        ws[f'A{row}'].border = thin_border
        
        ws[f'B{row}'] = desc
        ws[f'B{row}'].font = normal_font
        ws[f'B{row}'].alignment = left_alignment
        ws[f'B{row}'].border = thin_border
        
        ws.merge_cells(f'B{row}:D{row}')
    
    for row in range(6, 11):
        ws.row_dimensions[row].height = 22
    
    # 单位换算说明
    ws['A12'] = "②单位换算说明："
    ws['A12'].font = section_font
    ws.row_dimensions[12].height = 25
    
    ws.merge_cells('A13:D13')
    ws['A13'] = "根据检定/校准证书的计量单位和报告单位的需要，对测值进行单位换算。"
    ws['A13'].font = normal_font
    ws['A13'].alignment = left_alignment
    ws.row_dimensions[13].height = 22
    
    ws.merge_cells('A14:D14')
    ws['A14'] = "空气比释动能和周围剂量当量换算系数：使用¹³⁷Cs作为检定/校准参考辐射源时，换算系数取 1.20 Sv/Gy。"
    ws['A14'].font = normal_font
    ws['A14'].alignment = left_alignment
    ws.row_dimensions[14].height = 22
    
    # 设置列宽
    ws.column_dimensions['A'].width = 10
    ws.column_dimensions['B'].width = 45
    ws.column_dimensions['C'].width = 15
    ws.column_dimensions['D'].width = 15
    
    # 删除默认Sheet
    if 'Sheet' in wb.sheetnames:
        wb.remove(wb['Sheet'])

if __name__ == "__main__":
    create_excel_template()
