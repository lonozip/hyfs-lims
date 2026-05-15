import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Check for string values in base_value
cursor.execute("SELECT id, base_value FROM core_test WHERE typeof(base_value) = 'text'")
string_rows = cursor.fetchall()
print(f"String type base_value rows: {len(string_rows)}")
for row in string_rows[:20]:
    print(f"ID: {row[0]}, base_value: '{row[1]}', type: {type(row[1])}")

conn.close()