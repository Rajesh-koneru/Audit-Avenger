import mysql.connector
import os

#railway connection setUp

# Connect to the railway db
def get_connection():
    return mysql.connector.connect(
    host="crossover.proxy.rlwy.net",
    port=48804,
    user="root",
    password="dBHRfqBdPxdCVKoqsIirPjnOiOkCytBK",
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