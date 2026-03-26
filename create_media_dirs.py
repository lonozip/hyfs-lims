import os

# 创建 media 目录
if not os.path.exists('media'):
    os.makedirs('media')
    print('Created media directory')

# 创建 media/report_pdfs 目录
if not os.path.exists('media/report_pdfs'):
    os.makedirs('media/report_pdfs')
    print('Created media/report_pdfs directory')

print('Directories created successfully!')