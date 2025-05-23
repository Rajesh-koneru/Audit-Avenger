from flask import Flask ,redirect,render_template,Blueprint,request,jsonify,session,flash
import sqlite3
from flask_login import login_required,LoginManager,UserMixin,login_user
status=Blueprint('status' ,__name__)
import os
from audit_tarcker.config import get_connection


@status.route('/auditor/auditor_details')
def auditor_details():
    if session.get('role') == 'auditor':
        return jsonify({"username": session['username'], "id": session['id']})
    return jsonify({"error": "Unauthorized"}), 403

@status.route('/auditor/data',methods=["POST"])
@login_required
def status_update():
    try:
        data = request.get_json()
        print('this is received data', data)
        username = data['Id']
        password=data['username']
        print('this is username', username)
        query = f"SELECT * FROM audit_report WHERE auditor_id =%s "
        with get_connection() as conn:
            pointer = conn.cursor(dictionary=True)
            pointer.execute(query, (username,))
            row = pointer.fetchone()
            details=[]
            print(row)
            data1 = {'Audit_id': row['Audit_id'], 'auditor_name': row['auditor_name'],
                     'planned_date': row['planned_date'], 'state': row['State'],
                     'audit_status': row['Audit_status'], 'payment_amount': row['payment_amount'],
                     'payment_status': row['payment_status'], 'contact': row['Contact'],
                     'auditor_id': row['auditor_id'], 'audit_type': row['audit_type'],
                     'client_id': row['Client_id'], 'location': row['location'], 'email': row['email']}

        if data1:
            details.append(data1)
            return details
        else:
            return jsonify({"error": "No data found for this auditor"}),404
    except Exception as e:
        print(f"Error in status_update: {e}")
        return jsonify({"error": str(e)}), 500  # Always return a response


# auditor status update
@status.route('/auditor/status_update' ,methods=['POST'])
def update():
    try:
        data = request.get_json()
        audit_status = data['status']
        audit_id = data['id']
        print(audit_status)

        print('data received :', data)
        update = """update Audit_report set audit_status= %s where Audit_id=%s """
        with get_connection() as conn:
            pointer = conn.cursor(dictionary=True)
            pointer.execute(update, (audit_status, audit_id))
            pointer.execute(f'select * from audit_report  where Audit_id=?', (audit_id,))
            user = pointer.fetchone()
            print(f' updated at :{user}')
            return jsonify({"message": 'Status updated successfully....! Refresh the page...'})
    except Exception as e:
        print(e)
        return str(e)












