import pymysql

print("Testing root with no password...")
try:
    conn = pymysql.connect(host='localhost', user='root', password='', database='greentech_db')
    print("SUCCESS: Connected as root to greentech_db")
    conn.close()
except Exception as e:
    print(f"FAILED: {e}")

print("\nTesting root with 'green_tech' database...")
try:
    conn = pymysql.connect(host='localhost', user='root', password='', database='green_tech')
    print("SUCCESS: Connected as root to green_tech")
    conn.close()
except Exception as e:
    print(f"FAILED: {e}")
