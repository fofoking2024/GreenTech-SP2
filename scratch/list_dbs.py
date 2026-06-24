import pymysql

try:
    conn = pymysql.connect(host='localhost', user='root', password='')
    cursor = conn.cursor()
    cursor.execute("SHOW DATABASES")
    databases = [db[0] for db in cursor.fetchall()]
    print(f"Available databases: {databases}")
    conn.close()
except Exception as e:
    print(f"FAILED to connect: {e}")
