import sqlite3

# 连接到数据库
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

print("=== 检查core_standard表结构 ===")

# 1. 检查表的列信息
print("\n1. 表列信息:")
cursor.execute("PRAGMA table_info(core_standard)")
columns = cursor.fetchall()
for column in columns:
    print(f"  列名: {column[1]}, 类型: {column[2]}, 约束: {column[3]}")

# 2. 检查表的索引
print("\n2. 表索引:")
cursor.execute("PRAGMA index_list(core_standard)")
indexes = cursor.fetchall()
for index in indexes:
    index_id, index_name, unique, origin, partial = index
    print(f"  索引名: {index_name}, 唯一: {unique}")
    
    # 检查索引的列
    if index_name:
        cursor.execute(f"PRAGMA index_info({index_name})")
        index_columns = cursor.fetchall()
        for col in index_columns:
            print(f"    - 列: {col[2]}")

# 3. 尝试移除标准编号的唯一约束
print("\n3. 移除标准编号的唯一约束:")
try:
    # 查找标准编号的唯一索引
    cursor.execute("PRAGMA index_list(core_standard)")
    indexes = cursor.fetchall()
    
    for index in indexes:
        index_name = index[1]
        unique = index[2]
        
        if unique:
            # 检查索引包含的列
            cursor.execute(f"PRAGMA index_info({index_name})")
            index_columns = cursor.fetchall()
            
            for col in index_columns:
                col_name = col[2]
                if col_name == 'standard_id':
                    # 删除这个唯一索引
                    cursor.execute(f"DROP INDEX IF EXISTS {index_name}")
                    print(f"  已删除唯一索引: {index_name}")
                    break
    
    # 提交更改
    conn.commit()
    print("  操作完成")
except Exception as e:
    print(f"  错误: {e}")
finally:
    # 关闭连接
    conn.close()

print("\n=== 操作完成 ===")