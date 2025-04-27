from multiprocessing.connection import Client

from flask import Blueprint, request, jsonify
import sqlite3
import os
from datetime import datetime
from audit_tarcker.config import get_connection

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

        data = json_data["data"]  # Extract the array
        if data == " ":
            print("Received JSON is empty")  # Debugging
        print(data)
        conn=get_connection()
        cursor = conn.cursor()
        print('connected to my sql')

        for row in data:
            row = {key.strip(): value for key, value in row.items()}  # Strip spaces from keys
            print(row)
            planned_date = '2025-01-01'  # Default value
            Client_id = 1
            contact_number = int(row.get("Contact Number", "Unknown"))  # Handle missing keys safely

            cursor.execute("""
                INSERT INTO audit_report (Audit_id, auditor_name, planned_date, 
                                          State, City, Client_name, Client_id, Contact, Audit_status, 
                                          payment_amount, payment_status, track) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                row['Audit ID'], row['Auditor Name'], planned_date,
                row['State'], row['City'], row['Client Name'], Client_id, contact_number, row['Audit Status'],
                int(row['Payment Amount']), row['Payment Status'], row.get("Track", "Not Tracked")
            ))

        conn.commit()
        cursor.close()
        conn.close()
        print('data entered....')
        return jsonify({"message": "Data successfully saved to database!"})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500

