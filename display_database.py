import sqlite3
import json
import sys

# Path to the SQLite database
# Ensure this path is correct and accessible
DB_PATH = r"C:\Users\philip\AppData\Roaming\Cursor\User\globalStorage\state.vscdb"

# Connect to the database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Query to list all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

# Display all tables and their column names
for table in tables:
    table_name = table[0]
    print(f"\nTable: {table_name}")
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    column_names = [column[1] for column in columns]
    print("Columns:", column_names)

# Close the connection
conn.close()

print("\nDatabase column display complete.") 