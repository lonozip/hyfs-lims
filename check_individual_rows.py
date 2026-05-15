import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Try to identify which specific row causes the issue
cursor.execute("SELECT id, base_value FROM core_test ORDER BY id")
rows = cursor.fetchall()

print(f"Total rows: {len(rows)}")

# Check each row for potential issues
for i, row in enumerate(rows):
    row_id, base_value = row
    try:
        # Try to convert to float if it's not None
        if base_value is not None:
            float_val = float(base_value)
            print(f"Row {row_id}: OK - base_value={base_value}")
        else:
            print(f"Row {row_id}: OK - base_value=None")
    except Exception as e:
        print(f"Row {row_id}: ERROR - base_value={base_value}, error={e}")
        break

conn.close()