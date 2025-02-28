from flask import Flask ,redirect,render_template,Blueprint,request,jsonify,session,flash
import sqlite3
from flask_login import login_required,LoginManager,UserMixin,login_user
status=Blueprint('status' ,__name__)
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Get the directory of the current file
AuditTrack = os.path.join(BASE_DIR, '..', 'instance', 'auditTracker.db')

@status.route('/auditor/auditor_details')
def auditor_details():
    if session.get('role') == 'auditor':
        print( "this are details:",session['username'], session['id'])
        return jsonify({"username": session['username'], "id": session['id']})
    return jsonify({"error": "Unauthorized"}), 403



@status.route('/auditor/data',methods=["POST"])
@login_required
def status_update():
    try:
        data = request.get_json()
        print( 'this is received data',data)
        username=data['name'].upper()
        print( 'this is username',username)
        query = f"SELECT * FROM Audit_report WHERE auditor_name =? "
        with sqlite3.connect(AuditTrack) as conn:
            cursor = conn.cursor()
            cursor.execute(query ,(username,))
            row = cursor.fetchone()
            print(row)
            data1=[{'Audit_id':row[0],'auditor_name':row[1],'client_name':row[5],'planned_data':row[2],'state':row[3],'city':row[4],'audit_status':row[7],'payment_amount':row[8],'payment_status':row[9],'contact':row[6]}]
        if data1:
            return jsonify(data1)
        else:
            return jsonify({"error": "No data found for this auditor"}), 404

    except Exception as e:
        print(f"Error in status_update: {e}")
        return jsonify({"error": str(e)}), 500  # Always return a response


# auditor status update
@status.route('/auditor/status_update' ,methods=['POST'])
def update():
    try :
        data=request.get_json()
        audit_status=data['status']
        audit_id=data['id']
        print(audit_status)

        print('data received :', data)
        update="""update Audit_report set audit_status= ? where Audit_id=? """
        with sqlite3.connect(AuditTrack) as conn:
            pointer=conn.cursor()
            pointer.execute(update,(audit_status,audit_id))
            pointer.execute(f'select * from Audit_report  where Audit_id=?',(audit_id,))
            user=pointer.fetchone()
            print(f' updated at :{user}')
            return jsonify({"message":'Status updated successfully....! Refresh the page...'})
    except Exception as e:
        print(e)
        return str(e)




#auditor tracking :appending registered user to auditor database for tracking
@status.route('/auditor/log',methods=["POST"])
def auditor_log():
    data=request.get_json()
    if len(data)== ' ':
        return 'no data received! invalid json data '

    print('recieved data' ,data)
    name=data['name']
    Id=data['Id']
    review=data['review']

    query1="""select * from Auditor_data where Auditor_id=?"""
    query2="""update Auditor_data set number_of_audits=?, where Auditor_id=?"""
    query3="""insert into Auditor_data(Auditor_id,Auditor_name,number_of_audits,reviews) values(?,?,?,?)"""
    with sqlite3.connect(AuditTrack) as conn:
        pointer = conn.cursor()
        pointer.execute(query1, (Id,))
        user = pointer.fetchone()

        # checking user, if is present in the base then the details are updated else new record is created
        if user and len(user) !=0:
            try:
                pointer.execute(query2,(user[2]+1,Id))
                print('data updated...!')
            except Exception as e:
                print(e)
        else:
            try:
                pointer.execute(query3,(Id,name,1,review))
                print('data entered')
                return jsonify('data entered')
            except Exception as e:
                print(e)
                return f'error : str({e})'


















