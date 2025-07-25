import pymysql

def get_connection():
    return pymysql.connect(
        port=3306,
        host="localhost",
        user="root",
        password="12345",
        db="Docker MySQL",
        charset="utf-8"
    )