from pymongo.server_api import ServerApi
from pymongo import MongoClient

import os

# Use the correct MongoDB Atlas connection string
DATABASE_URL = "mongodb+srv://raghavendhargpth:MLOBWMCnt6VD9dkh@cluster0.9ipen.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Connect to MongoDB
try:
    client = MongoClient(DATABASE_URL, server_api=ServerApi('1'))
    db = client["AuditAvengers"]
    collection = db["Audit_Tracker"]
    collection.create_index("Audit_id", unique=True)

    print("✅ Connected to MongoDB")

except Exception as e:
    print("❌ Connection error:", e)




