import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Fix longitude field
cursor.execute("UPDATE core_test SET longitude = NULL WHERE longitude = ''")
print(f"Fixed {cursor.rowcount} rows in longitude field")

# Fix latitude field
cursor.execute("UPDATE core_test SET latitude = NULL WHERE latitude = ''")
print(f"Fixed {cursor.rowcount} rows in latitude field")

# Fix elevation field
cursor.execute("UPDATE core_test SET elevation = NULL WHERE elevation = ''")
print(f"Fixed {cursor.rowcount} rows in elevation field")

conn.commit()
conn.close()

print("All fixes applied successfully!")