import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Check all DecimalField columns for string values
decimal_columns = ['base_value', 'longitude', 'latitude', 'elevation']

for col in decimal_columns:
    cursor.execute(f"SELECT id, {col} FROM core_test WHERE typeof({col}) = 'text'")
    string_rows = cursor.fetchall()
    print(f"{col} - String type rows: {len(string_rows)}")
    for row in string_rows[:5]:
        print(f"  ID: {row[0]}, value: '{row[1]}'")

conn.close()