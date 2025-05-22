from flask import Flask ,Blueprint,redirect,jsonify,request
from flask_login import login_required
from audit_tarcker.config import get_connection
from datetime import datetime

report=Blueprint('report',__name__)

import sqlite3
import os
import sqlite3
import os


#BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Get the directory of the current file
#AuditTrack = os.path.join(BASE_DIR, '..', 'instance', 'auditTracker.db')

@report.route('/admin/report')
def admin_report():
    query = """ select * from audit_report"""
   # row=list(collection.find({},{"_id": 0}))query=""" select * from Audit_report"""

    conn=get_connection()

    pointer=conn.cursor()
    pointer.execute(query)

    row=pointer.fetchall()
    data=[]
    print(row)
    for i in range(len(row)):
        data1={'Audit_id':row[i]['Audit_id'],'auditor_name':row[i]['auditor_name'],'planned_date':row[i]['planned_date'],'state':row[i]['State'],'audit_status':row[i]['Audit_status'],'payment_amount':row[i]['payment_amount'],'payment_status':row[i]['payment_status'],'contact':row[i]['Contact'] ,'auditor_id':row[i]['auditor_id'],'audit_type':row[i]['audit_type'],'client_id':row[i]['Client_id'],'location':row[i]['location'],'email':row[i]['email']}
        data.append(data1)

    return jsonify(data)
# total number of audits
@report.route('/admin/total_audits')
def total_auditor():
    try:
        query = """select audit_id from Audit_report"""
        with get_connection() as conn:
            pointer=conn.cursor()
            pointer.execute(query)
            data = pointer.fetchall()
            total = 0
            for i in data:
                total += 1

            return jsonify(total)
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

# active audits
@report.route('/admin/active_audits')
def active_audits():
    try:
        query1 = """select audit_status from Audit_report where Audit_status='In Progress'"""
        with get_connection() as conn:
            pointer = conn.cursor()
            pointer.execute(query1)
            data1 = pointer.fetchall()
            total2 = 0
            for i in data1:
                total2 += 1

            return jsonify(total2)
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
# completed audits
@report.route('/admin/complete')
def complete():
    try:
        query2 = """select audit_status from Audit_report where Audit_status='Completed'"""
        with get_connection() as conn:
            pointer = conn.cursor()
            pointer.execute(query2)
            data1 = pointer.fetchall()
            total3 = 0
            for i in data1:
                total3 += 1

            return jsonify(total3)
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

#pending audits
@report.route('/admin/pending')
def pending():
    try:
        query3 = """select audit_status from Audit_report where Audit_status='Pending'"""
        with get_connection() as conn:
            pointer = conn.cursor()
            pointer.execute(query3)
            data1 = pointer.fetchall()
            total4 = 0
            for i in data1:
                total4 += 1

            return jsonify(total4)
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
# dashboard interaction
@report.route('/admin/Recent_audit')
def recent_audits():
    try:
        query4 = """select Audit_id,auditor_id,planned_Date, auditor_name,audit_status from audit_report limit 5 """
        with get_connection() as conn:
            pointer = conn.cursor()
            pointer.execute(query4)
            data1 = pointer.fetchall()
            print(data1)

            return jsonify(data1)
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
# filter data based on admin choice
@report.route('/admin/filter', methods=['POST'])
def filter_data():
    try:
        json_data = request.get_json()  # Get JSON data
        if not json_data or "data" not in json_data:
            return jsonify({"error": "Invalid JSON format, expected {'data': [...]}"}), 400

        value = json_data["data"]  # Extract the array
        print("Received JSON11:", json_data)  # Debugging

        if value=='Completed' or value=='Pending' or value=='In Progress':
            # data base query for filter data
            query4 = f"""select * from Audit_report where audit_status=%s """
            with get_connection() as conn:
                pointer = conn.cursor()
                pointer.execute(query4,(value,))
                data2 = pointer.fetchall()
                print(data2)
                return jsonify(data2)
        elif value=='Paid' or value=='Unpaid' or value=='Requested':
            # data base query for filter data
            query4 = f"""select * from Audit_report where payment_status=%s """
            with get_connection() as conn:
                pointer = conn.cursor()
                pointer.execute(query4, (value,))
                data2 = pointer.fetchall()
                print(data2)
                return jsonify(data2)
        else:
            # data base query for filter data
            query4 = f"""select * from Audit_report where State=%s """
            with get_connection() as conn:
                pointer = conn.cursor()
                pointer.execute(query4, (value,))
                data2 = pointer.fetchall()
                print(data2)
                return jsonify(data2)


    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


# admin manual updates auditors status if he is not update through app
@report.route('/admin/update_status' ,methods=["POST"])
def admin_status_update():
    try:
        data = request.get_json()
        print(data)
        value = data['Id']
        status = data['value']
        print(value)
        # data base manipulation

        update_query = f""" update Audit_report set audit_status=%s where auditor_id=%s"""
        with get_connection() as conn:
            pointer = conn.cursor()
            pointer.execute(update_query, (status, value))
            print('updated')
            return jsonify({"message": "database updated successfully..."})
    except Exception as e:
        return jsonify(e), 500

#admin payment status update
@report.route('/admin/update_payment' ,methods=['POST'])
def payment_update():
    try:
        data=request.get_json()

        value=data['Id']
        status=data['value']
        print(value,status)

        # data base manipulation
        update_query = f""" update Audit_report set payment_status=%s where auditor_id=%s"""
        with get_connection() as conn:
            pointer = conn.cursor()
            pointer.execute(update_query, (status, value))

        print('successfully updated')

        return jsonify({"message":"payment Status Updated successfully..."})
    except Exception as e:
        return jsonify(e) ,500

"""
# single record update in the database
@report.route('/admin/manual_update' ,methods=['POST'])
def manual_update():
    json_data=request.get_json()
    print(json_data)
    if json_data=='':
        print('no data received')
    data=json_data['data']
    print(data)
    try:
        date_str = data["Planned Date"]

        # Detect the format and parse accordingly
        if "-" in date_str:  # Example: 2025-03-20 (YYYY-MM-DD)
            planned_date = date_str  # Already correct, no conversion needed
        else:  # Example: 03/20/25 (MM/DD/YY)
            planned_date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")

        # Store the planned_date
        data["planned_date"] = planned_date

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    try:
        collection.insert_one(
            {
                "Audit_id": data["Audit Id"],
                "auditor_name": data["Auditor Name"],
                "client_name": data["Client Name"],
                "planned_date": datetime.strptime(data["Planned Date"], "%Y-%m-%d").strftime("%Y-%m-%d"),
                "state": data["State"],
                "city": data["City"],
                "auditor_contact": data.get("Contact",'N/A'),
                "audit_status": data["Audit Status"],
                "payment_amount": data["Payment Amount"],
                "payment_status": data["Payment Status"]
            })
        print('data inserted ')
        return jsonify('data inserted successfully...')
    except Exception as e:
        print(e)
        return jsonify(e) ,400

"""