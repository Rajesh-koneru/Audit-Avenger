from flask import Blueprint, request, jsonify
import sqlite3
import os
from audit_tarcker.config import collection

#BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Get the directory of the current file
#AuditTrack= os.path.join(BASE_DIR, '..', 'instance', 'auditTracker.db')


file = Blueprint('file',__name__)


@file.route('/upload-excel', methods=['POST'])
def upload_excel():
    if request.content_type != 'application/json':  # Ensure JSON format
        return jsonify({"error": "Content-Type must be application/json"}), 415

    try:
        json_data = request.get_json()  # Get JSON data
        if not json_data or "data" not in json_data:
            return jsonify({"error": "Invalid JSON format, expected {'data': [...]}"}), 400

        data = json_data["data"] # Extract the array
        if data==" ":
            print("Received JSON is empty")  # Debugging
        print(json_data)

        collection.insertMany([
            {
                "Audit_id": row["Audit ID"],
                "auditor_name": row["Auditor Name"],
                "client_name": row["Client Name"],
                "planned_date":row["planned_date"],
                "state": row["State"],
                "city": row["City"],
                "auditor_contact": row["Contact Number"],
                "audit_status": row["Audit Status"],
                "payment_amount": row["Payment Amount"],
                "payment_status": row[" Payment Status "]
            }
            for row in data  # Assuming data_list is a list of dictionaries
        ])

        print('data entered....!')
        return jsonify({"message": "Data successfully saved to database!"})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500
