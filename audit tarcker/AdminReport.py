from flask import Flask ,Blueprint,redirect,jsonify,request
report=Blueprint(__name__,'report')
import sqlite3
@report.route('/admin/report')
def admin_report():
    query=""" select * from Audit_report"""
    with sqlite3.connect('auditTracker.db') as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        row=cursor.fetchall()

        data=[]
        print(row)
        for i in range(len(row)):
            print(len(row))
            data1={'Audit_id':row[i][0],'auditor_name':row[i][1],'client_name':row[i][5],'planned_data':row[i][2],'state':row[i][3],'city':row[i][4],'audit_status':row[i][7],'payment_amount':row[i][8],'payment_status':row[i][9],'contact':row[i][6]}
            data.append(data1)
        print(data)
        return jsonify(data)

@report.route('/admin/total_audits')
def total_auditor():
    try:
        query="""select audit_id from Audit_report"""
        with sqlite3.connect('auditTracker.db') as conn:
            pointer=conn.cursor()
            pointer.execute(query)
            data=pointer.fetchall()
            total=0
            for i in data:
                total+=1
            print(total)
            return jsonify(total)
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
@report.route('/admin/active_audits')
def active_audits():
    try:
        query1="""select audit_status from Audit_report where Audit_status='In Progress'"""
        with sqlite3.connect('auditTracker.db') as conn:
            pointer=conn.cursor()
            pointer.execute(query1)
            data1=pointer.fetchall()
            total2=0
            for i in data1:
                total2+=1
            print(total2)
            return jsonify(total2)
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

@report.route('/admin/complete')
def complete():
    try:
        query2="""select audit_status from Audit_report where Audit_status='Completed'"""
        with sqlite3.connect('auditTracker.db') as conn:
            pointer=conn.cursor()
            pointer.execute(query2)
            data1=pointer.fetchall()
            total3=0
            for i in data1:
                total3+=1
            print(total3)
            return jsonify(total3)
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


@report.route('/admin/pending')
def pending():
    try:
        query3= """select audit_status from Audit_report where Audit_status='Pending'"""
        with sqlite3.connect('auditTracker.db') as conn:
            pointer = conn.cursor()
            pointer.execute(query3)
            data1 = pointer.fetchall()
            total4 = 0
            for i in data1:
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
        query4 ="""select client_name,planned_Date, auditor_name,Audit_status from Audit_report limit 5 """
        with sqlite3.connect('auditTracker.db') as conn:
            pointer = conn.cursor()
            pointer.execute(query4)
            data1 = pointer.fetchall()
            print(data1)

            return jsonify(data1)
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


@report.route('/admin/filter', methods=['POST'])
def filter_data():
    try:
        json_data = request.get_json()  # Get JSON data
        if not json_data or "data" not in json_data:
            return jsonify({"error": "Invalid JSON format, expected {'data': [...]}"}), 400

        value = json_data["data"]  # Extract the array
        print("Received JSON:", json_data)  # Debugging
        print(value)


        query4 =f"""select * from Audit_report where audit_status='{value}' """
        with sqlite3.connect('auditTracker.db') as conn:
            pointer = conn.cursor()
            pointer.execute(query4)
            data2 = pointer.fetchall()
            print(data2)
            return jsonify(data2)
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


