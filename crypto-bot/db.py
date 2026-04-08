import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",          # تغییر بده
        password="12345",          # رمز خودت را بگذار
        database="crypto_bot"
    )