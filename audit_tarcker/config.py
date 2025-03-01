import psycopg2
import os
from pymongo import MongoClient
import urllib.parse
username="raghavendhargpth"
password='Raghavendra@admin'

#encoded credentials
encoded_username = urllib.parse.quote_plus(username)
encoded_password = urllib.parse.quote_plus(password)

# Manually set the values from Render Dashboard
DATABASE_URL=os.getenv(f"mongodb+srv://raghavendhargpth:Raghavendra%40admin@cluster0.9ipen.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")


# Connect to MongoDB
mongo_client = MongoClient(DATABASE_URL)
db = mongo_client["AuditAvengers"]
collection = db["Audit_Tracker"]





"""row= list(collection.find({}, {"_id": 0}))
print(row)"""
"""audit_ids = list(collection.find({}, {"Audit_id": 1, "_id": 0}))
print(audit_ids)"""
"""
Active_record=list(collection.find({"Audit_id":"AA0001"},{"audit_status":0,"_id":0}))
print(Active_record)

recent_audit_report = list(
    collection.find({}, {"audit_status": 1, "client_name": 1, "planned_date": 1, "auditor_name": 1, "_id": 0}).limit(5))
print(recent_audit_report)

collection.update_one({"Audit_id":"AA0001"}, {"$set": {"audit_status": "Completed"}})
print("updated")
Active_record=list(collection.find({"Audit_id":"AA0001"},{"audit_status":1,"_id":0}))
print(Active_record)
"""

row=list(collection.find({"auditor_name":"RAJESH"},{"_id":0}))
print(row)
login_details = tuple(collection.find({"auditor_name": "hello"}, {"Audit_id": 1, "auditor_name": 1, "_id": 0}))
print(login_details)
print(login_details[0]["auditor_name"])


collection.insert_one(
    {
        "Audit_id":"AA0008",
        "auditor_name": "hello",
        "client_name":"AJAY&GROUPS",
        "planned_date": "25-4-3330"
,        "city": " City",
        "auditor_contact": " 98745537625",
        "audit_status": " pending",
        "payment_amount": "1000",
        "payment_status": " paid "
    })
print('data inserted')

"""# sql lite database
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Get the directory of the current file
AuditTrack = os.path.join(BASE_DIR, '..', 'instance', 'auditTracker.db')

"""