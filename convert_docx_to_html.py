import mammoth
import os
import sys
import io
import base64
import zipfile
import re

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    print("警告: Pillow 未安装")

if len(sys.argv) >= 2:
    docx_path = sys.argv[1]
else:
    docx_path = r"导入资料\20250813环境γ辐射剂量率检测报告模版.docx"

base_name = os.path.splitext(os.path.basename(docx_path))[0]
html_path = os.path.join(os.path.dirname(docx_path), f"{base_name}.html") if os.path.dirname(docx_path) else f"{base_name}.html"
image_dir = os.path.join(os.path.dirname(docx_path) or ".", "docx_images")
os.makedirs(image_dir, exist_ok=True)

image_map = {}

print("正在从 docx 中提取图片...")
with zipfile.ZipFile(docx_path, 'r') as z:
    media_files = [f for f in z.namelist() if f.startswith('word/media/')]
    print(f"  找到 {len(media_files)} 个媒体文件: {media_files}")

    for mf in media_files:
        data = z.read(mf)
        fname = os.path.basename(mf)
        ext = os.path.splitext(fname)[1].lower()

        r_id = None
        try:
            rels_data = z.read('word/_rels/document.xml.rels').decode('utf-8')
            import xml.etree.ElementTree as ET
            root = ET.fromstring(rels_data)
            ns = {'r': 'http://schemas.openxmlformats.org/package/2006/relationships'}
            for rel in root:
                target = rel.attrib.get('Target', '')
                if fname in target or target == mf or target == 'media/' + fname:
                    r_id = rel.attrib.get('Id', '')
                    break
        except:
            pass

        b64_str = None
        if HAS_PIL:
            try:
                img = Image.open(io.BytesIO(data))
                if img.mode in ("RGBA", "P", "CMYK"):
                    img = img.convert("RGBA")
                    fmt = "PNG"
                    mime = "image/png"
                else:
                    img = img.convert("RGB")
                    fmt = "JPEG"
                    mime = "image/jpeg"
                buf = io.BytesIO()
                img.save(buf, format=fmt, quality=90)
                b64_str = base64.b64encode(buf.getvalue()).decode("utf-8")
                embed_src = f"data:{mime};base64,{b64_str}"
                print(f"  转换成功: {fname} -> {mime}")
            except Exception as e:
                print(f"  转换失败: {fname}: {e}")
                b64_str = base64.b64encode(data).decode("utf-8")
                embed_src = f"data:image/png;base64,{b64_str}"
        else:
            b64_str = base64.b64encode(data).decode("utf-8")
            embed_src = f"data:image/png;base64,{b64_str}"

        image_map[fname] = embed_src
        if r_id:
            image_map[r_id] = embed_src


def convert_image(image):
    with image.open() as img_bytes:
        raw = img_bytes.read()

    content_type = image.content_type or ""
    alt_text = getattr(image, 'alt_text', '') or ''

    if HAS_PIL:
        try:
            img_obj = Image.open(io.BytesIO(raw))
            if img_obj.mode in ("RGBA", "P", "CMYK"):
                img_obj = img_obj.convert("RGBA")
                fmt = "PNG"
                mime = "image/png"
            else:
                img_obj = img_obj.convert("RGB")
                fmt = "JPEG"
                mime = "image/jpeg"
            buf = io.BytesIO()
            img_obj.save(buf, format=fmt, quality=90)
            b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
            src = f"data:{mime};base64,{b64}"
            return {"src": src, "alt": alt_text}
        except:
            pass

    b64 = base64.b64encode(raw).decode("utf-8")
    mime = content_type or "image/png"
    return {"src": f"data:{mime};base64,{b64}", "alt": alt_text}


style_map = """
p[style-name='Heading 1'] => h1:fresh
p[style-name='Heading 2'] => h2:fresh
p[style-name='Heading 3'] => h3:fresh
p[style-name='Heading 4'] => h4:fresh
p[style-name='Title'] => h1.title:fresh
b => strong
r[style-name='Strong'] => strong
table => table.table.table-bordered
"""

print("正在转换 docx -> HTML...")
with open(docx_path, "rb") as docx_file:
    result = mammoth.convert_to_html(
        docx_file,
        style_map=style_map,
        convert_image=mammoth.images.img_element(convert_image)
    )

html_content = result.value
warnings = result.messages

img_tag_count = html_content.count('<img')
base64_count = html_content.count('data:image')
print(f"  HTML中 <img> 标签数: {img_tag_count}")
print(f"  HTML中 base64 图片数: {base64_count}")

if img_tag_count == 0:
    print("正在手动替换图片占位符...")
    changed = 0
    for fname, src in image_map.items():
        if fname in html_content:
            img_tag = f'<img src="{src}" style="max-width:100%" />'
            html_content = html_content.replace(fname, img_tag)
            changed += 1
    print(f"  手动替换了 {changed} 个图片")

style_tag = """
<style>
    body {
        font-family: "SimSun", "宋体", serif;
        font-size: 14px;
        line-height: 1.8;
        color: #333;
        padding: 20px 40px;
        max-width: 210mm;
        margin: 0 auto;
    }
    h1, h2, h3, h4 {
        font-family: "SimHei", "黑体", sans-serif;
        text-align: center;
    }
    h1 { font-size: 22px; }
    h2 { font-size: 16px; }
    h3 { font-size: 14px; }
    h4 { font-size: 14px; }
    table.table-bordered {
        width: 100%;
        border-collapse: collapse;
        margin: 10px 0;
        font-size: 12px;
    }
    table.table-bordered td, table.table-bordered th {
        border: 1px solid #000;
        padding: 4px 6px;
        vertical-align: middle;
    }
    table.table-bordered th {
        background-color: #f5f5f5;
        font-weight: bold;
    }
    p {
        margin: 4px 0;
        text-indent: 0;
    }
    .title {
        font-size: 26px;
        font-weight: bold;
        text-align: center;
    }
    img {
        max-width: 100%;
        height: auto;
    }
    @media print {
        body { padding: 0; }
    }
</style>
"""

full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>环境γ辐射剂量率检测报告模版</title>
    {style_tag}
</head>
<body>
{html_content}
</body>
</html>
"""

with open(html_path, "w", encoding="utf-8") as f:
    f.write(full_html)

print(f"\n转换完成: {html_path}")
print(f"文件大小: {len(full_html):,} 字符")
print(f"<img> 标签: {full_html.count('<img')}")
if warnings:
    msgs = [w.message for w in warnings]
    important = [m for m in msgs if 'error' in m.lower() or 'fail' in m.lower()]
    if important:
        print(f"关键警告: {important}")
