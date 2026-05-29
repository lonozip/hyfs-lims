import os
import re
from docx import Document
from docx.shared import Pt, Inches, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from lxml import etree

SRC_FILE = r'd:\秦州_部门\孟令飞_LIMS\senaite.lims\senaite_lims\导入资料\20250813检测报告模版\20250813检测报告模版\20250813工频电磁场和噪声检测报告模版.docx'
OUT_DIR = r'd:\秦州_部门\孟令飞_LIMS\senaite.lims\senaite_lims\导入资料\20250813检测报告模版'
IMG_DIR = os.path.join(OUT_DIR, 'images_工频电磁场')

os.makedirs(IMG_DIR, exist_ok=True)

doc = Document(SRC_FILE)

WML_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'

img_counter = [0]
saved_images = {}

def extract_images_from_docx():
    for rel_id, rel in doc.part.rels.items():
        if "image" in str(rel.reltype):
            img_data = rel.target_part.blob
            ext = os.path.splitext(rel.target_ref)[1]
            img_counter[0] += 1
            fname = f'image_{img_counter[0]}{ext}'
            fpath = os.path.join(IMG_DIR, fname)
            with open(fpath, 'wb') as f:
                f.write(img_data)
            saved_images[rel_id] = fname
    print(f'Extracted {img_counter[0]} images to {IMG_DIR}')

extract_images_from_docx()

ALIGN_MAP = {
    WD_ALIGN_PARAGRAPH.CENTER: 'center',
    WD_ALIGN_PARAGRAPH.RIGHT: 'right',
    WD_ALIGN_PARAGRAPH.LEFT: 'left',
    WD_ALIGN_PARAGRAPH.JUSTIFY: 'justify',
    None: None
}

def get_alignment(p):
    return ALIGN_MAP.get(p.alignment, None)

def get_run_style_html(run):
    styles = []
    if run.bold:
        styles.append('font-weight:bold')
    if run.italic:
        styles.append('font-style:italic')
    if run.underline:
        styles.append('text-decoration:underline')
    if run.font.size:
        size_pt = run.font.size.pt
        styles.append(f'font-size:{size_pt}pt')
    font_name = run.font.name
    if font_name:
        styles.append(f'font-family:"{font_name}",SimSun,serif')
    if run.font.color and run.font.color.rgb:
        styles.append(f'color:#{run.font.color.rgb}')
    return '; '.join(styles)

IMAGES_ALREADY_EXTRACTED = set()

def extract_images_from_element(xml_element):
    """Extract image references from XML element. Deduplicates."""
    xml_str = etree.tostring(xml_element, encoding='unicode')
    imgs = []
    seen_in_this_call = set()

    for blip in re.finditer(r'r:embed="([^"]+)"', xml_str):
        embed = blip.group(1)
        if embed in saved_images and embed not in seen_in_this_call:
            seen_in_this_call.add(embed)
            fname = saved_images[embed]
            imgs.append(f'<img src="images_工频电磁场/{fname}" style="max-width:100%;height:auto;display:block;" />')

    return imgs

def paragraph_to_html(p, skip_images=False):
    align = get_alignment(p)
    align_style = f'text-align:{align};' if align else ''

    imgs = [] if skip_images else extract_images_from_element(p._element)
    has_text = any(run.text.strip() for run in p.runs)

    if imgs and not has_text:
        img_html = ''.join(imgs)
        return f'<div style="{align_style}">{img_html}</div>'

    if not p.text.strip() and not imgs:
        empty_runs = len(p.runs)
        if empty_runs == 0:
            return '<p style="min-height:0.5em;">&nbsp;</p>'
        return '<p style="min-height:1em;">&nbsp;</p>'

    runs_html = []
    for run in p.runs:
        text = run.text
        if not text:
            text = ''
        text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
        text = text.replace('\n', '<br/>')
        run_style = get_run_style_html(run)
        if run_style:
            runs_html.append(f'<span style="{run_style}">{text}</span>')
        else:
            runs_html.append(text)

    result = ''.join(runs_html)
    if imgs:
        result += ''.join(imgs)

    return f'<p style="{align_style}">{result}</p>'

def table_to_html(table, table_idx):
    rows = table.rows
    if len(rows) == 0:
        return ''

    cells_data = []
    for row in rows:
        row_cells = []
        for cell in row.cells:
            tc = cell._tc
            tc_pr = tc.find(qn('w:tcPr'))

            grid_span = 1
            vmerge = None
            if tc_pr is not None:
                gs = tc_pr.find(qn('w:gridSpan'))
                if gs is not None:
                    grid_span = int(gs.get(qn('w:val')))
                vm = tc_pr.find(qn('w:vMerge'))
                if vm is not None:
                    val = vm.get(qn('w:val'))
                    vmerge = 'restart' if val == 'restart' else 'continue'

            cell_imgs = extract_images_from_element(tc)
            used_img_embeds = set()

            cell_html_parts = []
            for p in cell.paragraphs:
                cell_html_parts.append(paragraph_to_html(p, skip_images=True))
            cell_html = ''.join(cell_html_parts)
            if cell_imgs:
                cell_html += '<div style="text-align:center;">' + ''.join(cell_imgs) + '</div>'

            row_cells.append({
                'html': cell_html,
                'grid_span': grid_span,
                'vmerge': vmerge
            })
        cells_data.append(row_cells)

    html = '<table class="report-table" style="border-collapse:collapse;width:100%;margin:8px 0;">'
    for ri, row_cells in enumerate(cells_data):
        html += '<tr>'
        for ci, cell in enumerate(row_cells):
            if cell['vmerge'] == 'continue':
                continue
            rowspan = 1
            if cell['vmerge'] == 'restart':
                rj = ri + 1
                while rj < len(cells_data):
                    if ci < len(cells_data[rj]) and cells_data[rj][ci]['vmerge'] == 'continue':
                        rowspan += 1
                        rj += 1
                    else:
                        break
            colspan = cell['grid_span'] if cell['grid_span'] > 1 else 1
            attrs = ''
            if colspan > 1:
                attrs += f' colspan="{colspan}"'
            if rowspan > 1:
                attrs += f' rowspan="{rowspan}"'
            html += f'<td style="border:1px solid #000;padding:4px 6px;vertical-align:middle;text-align:center;"{attrs}>{cell["html"]}</td>'
        html += '</tr>'
    html += '</table>'
    return html

def extract_body_elements():
    """Extract all body elements in order with their type info."""
    body = doc.element.body
    elements = []
    para_idx = 0
    table_idx = 0

    for child in body:
        tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
        if tag == 'p':
            if para_idx < len(doc.paragraphs):
                p = doc.paragraphs[para_idx]
                pPr = p._element.find(qn('w:pPr'))
                has_sect_pr = pPr is not None and pPr.find(qn('w:sectPr')) is not None
                elements.append({
                    'type': 'paragraph',
                    'data': p,
                    'section_break': has_sect_pr
                })
                para_idx += 1
        elif tag == 'tbl':
            if table_idx < len(doc.tables):
                elements.append({
                    'type': 'table',
                    'data': doc.tables[table_idx],
                    'index': table_idx,
                    'section_break': False
                })
                table_idx += 1
    return elements

def smart_split_pages(elements):
    """Split elements into A4 pages based on content structure."""
    pages = []
    current_page = []

    NEW_PAGE_BEFORE = ['四、检测结论', '附件', '报告说明', '一、仪器设备']

    def estimate_page_rows(page_els):
        """Estimate total row content on a page."""
        rows = 0
        for e in page_els:
            if e['type'] == 'table':
                rows += len(e['data'].rows)
            elif e['type'] == 'paragraph':
                text = e['data'].text.strip()
                if text:
                    rows += max(1, len(text) // 60)
        return rows

    def flush_page():
        nonlocal current_page
        if current_page:
            pages.append(current_page)
        current_page = []

    for i, el in enumerate(elements):
        text = ''
        if el['type'] == 'paragraph':
            text = el['data'].text.strip()

        # Split at section breaks
        if el['section_break']:
            if el['type'] == 'paragraph':
                current_page.append(el)
            flush_page()
            continue

        # Split before key content markers
        if any(text.startswith(h) for h in NEW_PAGE_BEFORE):
            flush_page()
            current_page = [el]
            continue

        # Smart table splitting: estimate content per page
        if el['type'] == 'table':
            table_rows = len(el['data'].rows)
            current_est = estimate_page_rows(current_page)

            # Large table alone on its own page
            if table_rows >= 10 and current_est > 0:
                flush_page()
                current_page = [el]
                continue

            # If adding this table would exceed ~35 row equivalent, split
            if current_est + table_rows > 35 and current_est > 0:
                flush_page()
                current_page = [el]
                continue

            # If current page has 2+ tables and this is a significant table
            table_count = sum(1 for e in current_page if e['type'] == 'table')
            if table_count >= 2 and table_rows > 3:
                flush_page()
                current_page = [el]
                continue

        current_page.append(el)

    flush_page()

    # Merge empty pages with next page
    merged = []
    skip_next = False
    for i, page in enumerate(pages):
        if skip_next:
            skip_next = False
            continue
        # Check if page is essentially empty (only blank paragraphs)
        has_content = any(
            (e['type'] == 'paragraph' and e['data'].text.strip()) or
            e['type'] == 'table'
            for e in page
        )
        if not has_content and i + 1 < len(pages):
            pages[i + 1] = page + pages[i + 1]
            skip_next = False
            continue
        merged.append(page)

    return merged

elements = extract_body_elements()
print(f'Total body elements: {len(elements)}')

pages = smart_split_pages(elements)
print(f'Total pages: {len(pages)}')
for i, page in enumerate(pages):
    paras = sum(1 for e in page if e['type'] == 'paragraph')
    tables = sum(1 for e in page if e['type'] == 'table')
    first_text = ''
    for e in page:
        if e['type'] == 'paragraph' and e['data'].text.strip():
            first_text = e['data'].text.strip()[:60]
            break
    print(f'  Page {i+1}: {paras} paras, {tables} tables - starts: "{first_text}"')

A4_CSS = """
        @page {
            size: A4;
            margin: 2cm 1.8cm 2cm 1.8cm;
        }
        @media print {
            body {
                margin: 0;
                padding: 0;
            }
            .page-container {
                width: 100%;
                max-width: 100%;
                margin: 0;
                padding: 0;
                box-shadow: none;
            }
        }
        @media screen {
            body {
                background: #e8e8e8;
                display: flex;
                flex-direction: column;
                align-items: center;
                padding: 20px;
            }
            .page-container {
                width: 210mm;
                min-height: 297mm;
                background: #fff;
                padding: 2cm 1.8cm;
                margin-bottom: 20px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.15);
                overflow-y: auto;
            }
        }
        * {
            box-sizing: border-box;
        }
        body {
            font-family: SimSun, "宋体", "Times New Roman", serif;
            font-size: 12pt;
            color: #000;
            line-height: 1.6;
        }
        .page-container p {
            margin: 0.3em 0;
            line-height: 1.6;
        }
        table.report-table {
            width: 100% !important;
            border-collapse: collapse;
            margin: 8px 0;
            font-size: 10.5pt;
        }
        table.report-table td, table.report-table th {
            border: 1px solid #000;
            padding: 4px 6px;
            vertical-align: middle;
            line-height: 1.5;
        }
        table.report-table p {
            margin: 2px 0;
        }
"""

def render_page(page_elements, page_num):
    body_html = ''
    for el in page_elements:
        if el['type'] == 'paragraph':
            body_html += paragraph_to_html(el['data'])
        elif el['type'] == 'table':
            body_html += table_to_html(el['data'], el['index'])

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>检测报告 - 第{page_num}页</title>
<style>
{A4_CSS}
</style>
</head>
<body>
<div class="page-container">
{body_html}
</div>
</body>
</html>'''
    return html

# Clear old HTML files
for f in os.listdir(OUT_DIR):
    if f.startswith('工频电磁场和噪声检测报告_第') and f.endswith('.html'):
        os.remove(os.path.join(OUT_DIR, f))

for i, page in enumerate(pages):
    fname = f'工频电磁场和噪声检测报告_第{i+1}页.html'
    fpath = os.path.join(OUT_DIR, fname)
    html_content = render_page(page, i + 1)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f'Created: {fname} ({len(html_content)} chars)')

print(f'\nDone! Generated {len(pages)} HTML files.')
print(f'Images folder: {IMG_DIR}')
