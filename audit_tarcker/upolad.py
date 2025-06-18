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
            date_str = row["Date"]

            # Detect the format and parse accordingly
            if "-" in date_str:  # Example: 2025-03-20 (YYYY-MM-DD)
                date = date_str  # Already correct, no conversion needed
            else:  # Example: 03/20/25 (MM/DD/YY)
                date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")

            # Store the planned_date
            row["Date"] = date


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
                           Client_id,
                           whatsappLink
                       ) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            with get_connection() as conn:
                pointer = conn.cursor(dictionary=True)
                pointer.execute(query, (
                row['Audit_id'], row['Audit Type'], row['audit industry'], row['Date'], row['auditors require'],
                row['days'], row['qualification'], row['equipment'], row['location'], row['state'], row['amount'],
                row['client Id'], row['whatsapp link']))
            # <- Optional 'track'
        print('data entered....')
        return jsonify({"message": "Data successfully saved to database!"})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500

