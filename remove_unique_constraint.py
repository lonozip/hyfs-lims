import sqlite3

# 连接到数据库
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# 检查是否存在唯一性约束
try:
    # 获取表的索引信息
    cursor.execute("PRAGMA index_list(core_standard)")
    indexes = cursor.fetchall()
    
    # 查找标准编号的唯一索引
    for index in indexes:
        index_name = index[1]
        if 'standard_id' in index_name and 'unique' in index_name.lower():
            # 删除唯一索引
            cursor.execute(f"DROP INDEX IF EXISTS {index_name}")
            print(f"已删除唯一索引: {index_name}")
            break
    
    # 提交更改
    conn.commit()
    print("数据库修改成功")
except Exception as e:
    print(f"错误: {e}")
finally:
    # 关闭连接
    conn.close()