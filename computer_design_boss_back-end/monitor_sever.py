# monitor.py - 每10秒检查一次连接状态
import time
import pymysql

def check_connections():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='123456',
        database='boss_job'
    )
    cursor = conn.cursor()
    cursor.execute("SHOW PROCESSLIST")
    count = len(cursor.fetchall())
    cursor.close()
    conn.close()
    return count

while True:
    count = check_connections()
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] MySQL连接数: {count}")
    time.sleep(600)