from flask import Blueprint, request, jsonify
import sqlite3

file = Blueprint(__name__, 'file')


@file.route('/upload-excel', methods=['POST'])
def upload_excel():
    if request.content_type != 'application/json':  # Ensure JSON format
        return jsonify({"error": "Content-Type must be application/json"}), 415

    try:
        json_data = request.get_json()  # Get JSON data
        if not json_data or "data" not in json_data:
            return jsonify({"error": "Invalid JSON format, expected {'data': [...]}"}), 400

        data = json_data["data"]  # Extract the array
        print("Received JSON:", json_data)  # Debugging

        conn = sqlite3.connect("auditTracker.db")
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

        return jsonify({"message": "Data successfully saved to database!"})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500
