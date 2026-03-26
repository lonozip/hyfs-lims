import sqlite3

# 连接到数据库
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

print("=== 移除标准编号的唯一约束 ===")

try:
    # 1. 创建一个新表，结构与旧表相同，但标准编号没有唯一约束
    print("1. 创建新表...")
    cursor.execute('''
    CREATE TABLE core_standard_new (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(255) NOT NULL,
        standard_type VARCHAR(255) NOT NULL,
        standard_id VARCHAR(50) NOT NULL,
        collection_date DATETIME NOT NULL,
        status VARCHAR(20) NOT NULL,
        created_at DATETIME NOT NULL,
        updated_at DATETIME NOT NULL,
        created_by_id INTEGER,
        description TEXT NOT NULL,
        test_name VARCHAR(255) NOT NULL,
        unit VARCHAR(50) NOT NULL,
        acceptance_reference_range VARCHAR(100) NOT NULL,
        stability_reference_range VARCHAR(100) NOT NULL,
        status_reference_range VARCHAR(100) NOT NULL,
        FOREIGN KEY (created_by_id) REFERENCES auth_user (id)
    )
    ''')
    
    # 2. 复制数据从旧表到新表
    print("2. 复制数据...")
    cursor.execute('''
    INSERT INTO core_standard_new (
        id, name, standard_type, standard_id, collection_date, status, 
        created_at, updated_at, created_by_id, description, test_name, 
        unit, acceptance_reference_range, stability_reference_range, 
        status_reference_range
    ) SELECT 
        id, name, standard_type, standard_id, collection_date, status, 
        created_at, updated_at, created_by_id, description, test_name, 
        unit, acceptance_reference_range, stability_reference_range, 
        status_reference_range
    FROM core_standard
    ''')
    
    # 3. 删除旧表
    print("3. 删除旧表...")
    cursor.execute('DROP TABLE core_standard')
    
    # 4. 将新表重命名为旧表的名称
    print("4. 重命名新表...")
    cursor.execute('ALTER TABLE core_standard_new RENAME TO core_standard')
    
    # 5. 重新创建必要的索引
    print("5. 重新创建索引...")
    cursor.execute('CREATE INDEX core_standard_created_by_id_a17709c4 ON core_standard (created_by_id)')
    
    # 提交更改
    conn.commit()
    print("\n操作成功！标准编号的唯一约束已移除")
    
except Exception as e:
    print(f"\n错误: {e}")
    # 回滚更改
    conn.rollback()
finally:
    # 关闭连接
    conn.close()

print("\n=== 操作完成 ===")