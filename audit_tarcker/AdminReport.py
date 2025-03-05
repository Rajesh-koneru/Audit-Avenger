from flask import Flask ,Blueprint,redirect,jsonify,request
from flask_login import login_required
from audit_tarcker.config import collection
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

    row=list(collection.find({},{"_id": 0}))


    return jsonify(row)
# total number of audits
@report.route('/admin/total_audits')
def total_auditor():
    try:

        audit_ids = list(collection.find({}, {"Audit_id": 1, "_id": 0}))
        total=0
        for i in audit_ids:
            total+=1
        print(total)
        return jsonify(total)
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

# active audits
@report.route('/admin/active_audits')
def active_audits():
    try:
        query1="""select audit_status from Audit_report where Audit_status='In Progress'"""
        Active_record=list(collection.find({"audit_status":"In Progress"},{"audit_status":1,"_id":0}))
        total2=0
        for i in Active_record:
            total2+=1
        print(total2)
        return jsonify(total2)
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
# active audits
@report.route('/admin/complete')
def complete():
    try:
        Complete_status=list(collection.find({"audit_status":"Completed"},{"audit_status":1,"_id":0}))
        total3=0
        for i in  Complete_status :
            total3+=1
        print(total3)
        return jsonify(total3)
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

#pending audits
@report.route('/admin/pending')
def pending():
    try:

        pending_report=list(collection.find({"audit_status":"Pending"},{"audit_status":1,"_id":0}))
        total4 = 0
        for i in pending_report:
            total4 += 1
        print(total4)

        return jsonify(total4)
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
# dashboard interaction
@report.route('/admin/Recent_audit')
def recent_audits():
    try:
        recent_audit_report=list(collection.find({},{"audit_status":1,"client_name":1,"planned_date":1,"auditor_name":1, "_id":0}).limit(5))
        print("printing recent audits")
        print(recent_audit_report)

        return jsonify(recent_audit_report)
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
        print(value)

# data base query for filter data
        filter_data=list(collection.find({"audit_status":value},{"_id":0}))

        print(filter_data)
        return jsonify(filter_data)
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

# admin manual updates auditors status if he is not update through app
@report.route('/admin/update_status' ,methods=["POST"])
def admin_status_update():
    try:
        data=request.get_json()
        print(data)
        value=data['Id']
        status=data['value']
        print(value)
        # data base manipulation

        collection.update_one({"Audit_id":value},{"$set":{"audit_status":status}})
        print('updated')
        return jsonify({"message":"database updated successfully..."})
    except Exception as e:
        return jsonify(e) ,500

@report.route('admin/manual_update' ,methods=['post'])
def manual_update():
    json_data=request.get_json()
    if json_data=='':
        print('no data received')
    data=json_data['data']
    print(data)
    try:
        collection.insert_one(
            {
                "Audit_id": data["Audit ID"],
                "auditor_name": data["Auditor Name"],
                "client_name": data["Client Name"],
                "planned_date": datetime.strptime(data[" Planned Date"], "%m/%d/%y").strftime("%Y-%m-%d"),
                "state": data["State"],
                "city": data[" City"],
                "auditor_contact": data[" Contact Number"],
                "audit_status": data[" Audit Status"],
                "payment_amount": data["Payment Amount"],
                "payment_status": data[" Payment Status "]
            })
        print('data inserted ')
        return jsonify('data inserted successfully...')
    except Exception as e:
        print(e)
        return jsonify(e) ,400



