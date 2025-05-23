from multiprocessing.connection import Client

from flask import Blueprint, request, jsonify
import sqlite3
import os
from datetime import datetime
from audit_tarcker.config import get_connection



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


        for row in data:
            row = {key.strip(): value for key, value in row.items()}  # Strip spaces from keys
            print(row)
            planned_date = '2025-01-01'  # Default value
            Client_id = 1
            contact_number = int(row.get("Contact Number", "Unknown"))  # Handle missing keys safely

            query = """insert into audit_details(
                           Audit_id,
                           Audit_type,
                           industry,
                           Date,
                           Auditors_require,
                           Days,
                           Qualification,
                           equipment,
                           loction,
                           state,
                           Amount,
                           requirements,
                           Client_id,
                           WhatsappLink
                       ) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            with get_connection() as conn:
                pointer = conn.cursor(dictionary=True)
                pointer.execute(query, (
                row['Audit Id'], row['Auditor type'], row['industry'], row['Date'], row['auditor require'],
                row['Day'], row['Qualification'], row['equipment'], row['location'], row['State'], row['Amount'],
                row['requirement'], row['client_id'], row['whatsapp']))
            # <- Optional 'track'
        print('data entered....')
        return jsonify({"message": "Data successfully saved to database!"})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500

