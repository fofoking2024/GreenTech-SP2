"""
Setup script: creates the greentech_db MySQL database and all tables.
Run once before starting the Flask app.
"""
import pymysql

print("Connecting to MySQL...")
conn = pymysql.connect(host='localhost', user='root', password='')
cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS greentech_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
cursor.execute("SHOW DATABASES LIKE 'greentech_db'")
result = cursor.fetchone()
print(f"Database status: {result}")
conn.commit()
conn.close()
print("greentech_db is ready.")

print("\nCreating all tables via Flask-SQLAlchemy...")
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app
app = create_app()
with app.app_context():
    from extensions import db
    db.create_all()
    print("All tables created successfully!")

print("\nDone! You can now run: python app.py")
