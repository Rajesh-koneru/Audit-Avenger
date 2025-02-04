from flask import Flask,jsonify,Blueprint,request
import sqlite3

audit_status=Blueprint(__name__,'status')

@audit_status.route('/auditor/audit_status' ,methods=['POST'])
def status_repo():
    auditor_name=request.form.get('name')
    auditor_id=request.form.get('id')
    payment_status=request.form.get('pay')
    audit_status=request.form.get('status')

    query="""update audit_report set audit_status=?,audit_payment=? where auditor_id=?"""
    values = [audit_status,payment_status,auditor_id ]
    with sqlite3.connect('auditTracker.db') as conn:
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()  # ensure data saved
        data = cursor.fetchall()
        print(data)
        print('data updated')
        return 'data updated'



