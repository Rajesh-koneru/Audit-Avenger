from flask import Blueprint, request, jsonify
import sqlite3
import os
from audit_tarcker.config import AuditTrack

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

        conn = sqlite3.connect(AuditTrack)
        cursor = conn.cursor()

        for row in data:
            # Ensure no extra spaces in keys
            planned_date = row[' Planned Date'].strip() if row['Planned Date'] else '2025-01-01'  # Default value

            cursor.execute("""
                INSERT INTO Audit_report (Audit_id, auditor_name, client_name, planned_date, 
                                         state, city, auditor_contact, audit_status, 
                                         payment_amount, payment_status) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                row['Audit ID'], row['Auditor Name'], row['Client Name'], planned_date,
                row['State'], row[' City'], row[' Contact Number'], row[' Audit Status'],
                row['Payment Amount'], row[' Payment Status ']
            ))

        conn.commit()  # Remove extra comma
        conn.close()
        print('data entered....!')
        return jsonify({"message": "Data successfully saved to database!"})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500
