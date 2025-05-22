import mysql.connector
import os

# Connect to the railway db
def get_connection():
    return mysql.connector.connect(
    host="interchange.proxy.rlwy.net",
    port=20639,
    user="root",
    password="nwPKmzXjMQOHkjlaGLndEYiCwXuOOBTa",
    database="railway"
)





