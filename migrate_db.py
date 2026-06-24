"""
Migration script: adds missing columns to existing tables.
Safe to run multiple times — checks before adding each column.
"""
import pymysql

print("Connecting to MySQL greentech_db...")
conn = pymysql.connect(host='localhost', user='root', password='', database='greentech_db')
cursor = conn.cursor()

# --- Check current columns in 'request' table ---
cursor.execute("DESCRIBE `request`")
existing_cols = [row[0] for row in cursor.fetchall()]
print(f"Existing columns in 'request': {existing_cols}")

# --- Columns to add if missing ---
migrations = [
    ("ai_summary",      "ALTER TABLE `request` ADD COLUMN `ai_summary` TEXT NULL"),
    ("ai_conversation", "ALTER TABLE `request` ADD COLUMN `ai_conversation` TEXT NULL"),
    ("latitude",        "ALTER TABLE `request` ADD COLUMN `latitude` FLOAT NULL"),
    ("longitude",       "ALTER TABLE `request` ADD COLUMN `longitude` FLOAT NULL"),
    ("address",         "ALTER TABLE `request` ADD COLUMN `address` VARCHAR(255) NULL"),
]

for col_name, sql in migrations:
    if col_name not in existing_cols:
        print(f"  Adding column '{col_name}'...")
        cursor.execute(sql)
        conn.commit()
        print(f"  [ADDED] Column '{col_name}' added.")
    else:
        print(f"  [OK]    Column '{col_name}' already exists, skipping.")

# --- Verify all tables exist ---
cursor.execute("SHOW TABLES")
tables = [row[0] for row in cursor.fetchall()]
print(f"\nAll tables in greentech_db: {tables}")

cursor.execute("DESCRIBE `request`")
final_cols = [row[0] for row in cursor.fetchall()]
print(f"Final columns in 'request': {final_cols}")

conn.close()
print("\n[DONE] Migration complete! All columns are up to date.")
