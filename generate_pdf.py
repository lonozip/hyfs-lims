import requests

# 访问生成 PDF 报告的 URL
try:
    response = requests.get('http://127.0.0.1:8000/reports/6/generate_pdf/')
    print(f'Response status code: {response.status_code}')
    print(f'Response content: {response.text}')
except Exception as e:
    print(f'Error: {e}')