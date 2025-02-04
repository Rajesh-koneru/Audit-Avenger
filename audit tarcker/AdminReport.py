from flask import Flask ,Blueprint,redirect
report=Blueprint(__name__,'report')
import sqlite3
@report.route('/admin/report')
def admin_report():
    query=""" select * from audit_report"""
    with sqlite3.connect('auditTracker.db') as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()


