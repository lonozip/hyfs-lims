import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Check for invalid base_value data
cursor.execute("SELECT id, base_value FROM core_test WHERE typeof(base_value) != 'integer' AND typeof(base_value) != 'real'")
invalid_rows = cursor.fetchall()
print('Invalid base_value rows:', len(invalid_rows))
for row in invalid_rows[:20]:
    print(f'ID: {row[0]}, base_value: {row[1]}, type: {type(row[1])}')

conn.close()