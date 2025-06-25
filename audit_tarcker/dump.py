import mysql.connector
import os

# Use keyword arguments instead of full URL
conn = mysql.connector.connect(
    host="yamanote.proxy.rlwy.net",
    port=31145,
    user="root",
    password="ZuKHpINqyWjNuXtAUTeXgAJGdQfaFmme",
    database="railway"
)

print("Database connected...")

cursor = conn.cursor(dictionary=True)

with open(r"C:\Users\user\PycharmProjects\flaskApp\Dump20250618\audittracker_auditreport.sql", "r") as f:
    sql = f.read()
    for statement in sql.split(';'):
        if statement.strip():
            cursor.execute(statement)

conn.commit()
cursor.close()
conn.close()

print("Import completed.")
