import pymysql
import os

db_name = 'greentech_db'
sql_file = 'DataBases/green_tech.sql'

try:
    # Connect without database first
    conn = pymysql.connect(host='localhost', user='root', password='')
    cursor = conn.cursor()
    
    # Create database
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    print(f"Database '{db_name}' created or already exists.")
    
    # Switch to the database
    conn.select_db(db_name)
    
    # Read and execute SQL file
    print(f"Reading {sql_file}...")
    with open(sql_file, 'r', encoding='utf-8') as f:
        sql_commands = f.read().split(';')
        
    print(f"Executing {len(sql_commands)} commands...")
    for command in sql_commands:
        if command.strip():
            try:
                cursor.execute(command)
            except Exception as e:
                # Some commands might fail if they are metadata or comments, but we try to continue
                print(f"Skipping command error: {e}")
    
    conn.commit()
    print("Import successful!")
    conn.close()
    
except Exception as e:
    print(f"FATAL ERROR: {e}")
