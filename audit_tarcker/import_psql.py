import sqlite3
from pymongo import MongoClient
import urllib.parse

from audit_tarcker.config import AuditTrack

# Step 1: Connect to SQLite
sqlite_conn = sqlite3.connect(AuditTrack)  # Replace with your SQLite file
cursor = sqlite_conn.cursor()

username="raghavendhargpth"
password='Raghavendra@admin'

#encoded credentials
encoded_username = urllib.parse.quote_plus(username)
encoded_password = urllib.parse.quote_plus(password)
# Step 2: Connect to MongoDB
MONGO_URI = f"mongodb+srv://{encoded_username}:{encoded_password}@cluster0.9ipen.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client["AuditAvengers"]  # Change database name
mongo_collection = mongo_db["Audit_Tracker"]  # Change collection name

# Step 3: Get all tables in SQLite
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Step 4: Loop through all tables and migrate data
for table in tables:
    table_name = table[0]
    print(f"Migrating table: {table_name}")

    # Fetch data from SQLite table
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    # Get column names
    column_names = [desc[0] for desc in cursor.description]

    # Convert SQLite rows to MongoDB documents
    documents = []
    for row in rows:
        doc = {column_names[i]: row[i] for i in range(len(column_names))}
        documents.append(doc)

    # Insert documents into MongoDB
    if documents:
        mongo_collection.insert_many(documents)
        print(f"Inserted {len(documents)} records from {table_name} to MongoDB!")

# Step 5: Close connections
cursor.close()
sqlite_conn.close()
mongo_client.close()
print("Migration completed successfully!")
