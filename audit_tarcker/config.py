from pymongo.server_api import ServerApi
from pymongo import MongoClient

import os

# Use the correct MongoDB Atlas connection string
DATABASE_URL = os.getenv("DATABASE_URL1")

# Connect to MongoDB
try:
    client = MongoClient(DATABASE_URL, server_api=ServerApi('1'))
    db = client["AuditAvengers"]
    collection = db["Audit_Tracker"]
    collection.create_index("Audit_id", unique=True)
    test_data = collection.find_one()
    print("MongoDB Test Query Result:", test_data)

    print("✅ Connected to MongoDB")

except Exception as e:
    print("❌ Connection error:", e)




