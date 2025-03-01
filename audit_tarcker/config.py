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
    print("✅ Connected to MongoDB")

except Exception as e:
    print("❌ Connection error:", e)

# Fetch all records
row = list(collection.find({"auditor_name": "RAJESH"}, {"_id": 0}))
print("RAJESH's audits:", row)

# Handle empty results safely
login_details = list(collection.find({"auditor_name": "hello"}, {"Audit_id": 1, "auditor_name": 1, "_id": 0}))
if login_details:
    print("Auditor:", login_details[0]["auditor_name"])
else:
    print("No login details found.")

# Insert data
collection.insert_one(
    {
        "Audit_id": "AA0008",
        "auditor_name": "hello",
        "client_name": "AJAY&GROUPS",
        "planned_date": "25-4-3330",
        "city": "City",
        "auditor_contact": "98745537625",
        "audit_status": "pending",
        "payment_amount": "1000",
        "payment_status": "paid"
    }
)
print("✅ Data inserted")
