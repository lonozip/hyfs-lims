import re
import os

html_path = os.path.join(os.path.dirname(__file__), '导入资料', '20250813环境γ辐射剂量率检测报告模版.html')
out_path = os.path.join(os.path.dirname(__file__), '导入资料', 'logo_base64.txt')

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

imgs = re.findall(r'<img[^>]+src="(data:image/[^"]+)"', html)
if imgs:
    with open(out_path, 'w', encoding='utf-8') as out:
        out.write(imgs[0])
    print(f'Logo extracted: {len(imgs[0])} chars -> {out_path}')
else:
    print('No images found in HTML')
