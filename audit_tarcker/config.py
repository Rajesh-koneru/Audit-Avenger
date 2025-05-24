import mysql.connector
import os

#railway connection setUp

# Connect to the railway db
def get_connection():
    return mysql.connector.connect(
    host="interchange.proxy.rlwy.net",
    port=20639,
    user="root",
    password="nwPKmzXjMQOHkjlaGLndEYiCwXuOOBTa",
    database="railway",
    autocommit = True
   )

 #Connect to PlanetScale
"""def get_connection():
    return mysql.connector.connect(
    host="127.0.0.1",
    user="raju",
    password="Bujji@192921",
    database="AuditTracker",
    autocommit = True  # Ensures automatic commit
)"""