from flask import Flask ,Blueprint,redirect,jsonify,request
from flask_login import login_required
import threading
import time
import queue
from audit_tarcker.config import get_connection
from datetime import datetime
application=Blueprint('application',__name__)
@application.route('/admin/application')
def admin_report():
    query = """ select * from applications"""

    conn=get_connection()

    pointer=conn.cursor(dictionary=True)
    pointer.execute(query)

    row=pointer.fetchall()
    print('the db data',row)
    data=[]

    for i in range(len(row)):
        data1={'Audit_id':row[i]['audit_id'],'Auditor_id':row[i]['Auditor_id'],'Auditor_name':row[i]["Auditor_name"],'audit_type':row[i]['audit_type'],'Date':row[i]['date'],'phone':row[i]['phone'],'email':row[i]['email'],'Client_id':row[i]['client_id'],'state':row[i]['state']}
        data.append(data1)

    return jsonify(data)

@application.route("/applications/status" ,methods=["PUT",'POST'])
def status_update():
    try:
        #received data from frontend
        data=request.get_json()
        print(data)
        auditor_id=data['Id']
        status=data['status']
        query="""update applications set status=%s where Auditor_id=%s"""
        with get_connection() as conn:
            pointer = conn.cursor(dictionary=True)
            pointer.execute(query,(status,auditor_id))
            print('status updated successfully')
            conn.commit()
        return jsonify({'message':"status updated successfully "})
    except Exception as e:
        print(str(e))
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

# root for application clean up from application table and adding the into audit report table
@application.route('/application/audit_report', methods=['POST'])
def report():
    try:
        data = request.get_json()
        print("Received data:", data)

        if isinstance(data, dict):
            data = [data]  # Convert single object to list

        with get_connection() as conn:
            pointer = conn.cursor(dictionary=True)

            for row in data:
                state = row.get('status')

                if state == 'Accepted':
                    # Clean keys
                    row = {key.strip(): value for key, value in row.items()}
                    print('The single data is:', row)

                    if 'Date' not in row:
                        return jsonify({"error": "Missing 'Date' field."}), 400

                    planned_date = clean_date(row['Date'])
                    print('Planned Date:', planned_date)

                    location = loca(row['audit_id'])
                    print("Location details:", location)

                    aud_id = auditor_id()

                    # Check for required keys
                    required_keys = [
                        'audit_id', 'auditor_name', 'Date', 'state', 'audit_type',
                        'auditor_id', 'client_id', 'phone', 'email', 'payment'
                    ]
                    if not all(k in row for k in required_keys):
                        return jsonify({"error": f"Missing required fields in: {row}"}), 400

                    # Insert into audit_report
                    pointer.execute("""
                        INSERT INTO audit_report (
                            Audit_id, auditor_id, planned_date,
                            State, Client_id, Contact, Audit_status, 
                            payment_amount, payment_status, auditor_name, audit_type, location, email
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        row["audit_id"], aud_id, planned_date, row['state'],
                        row['client_id'], row['phone'], 'pending',
                        row['payment'], 'pending', row['auditor_name'],
                        row['audit_type'], location.get('loction'), row['email']
                    ))
                    conn.commit()

                    # Start background threads
                    result_queue = queue.Queue()
                    threading.Thread(target=delete_audit_data, args=(data, result_queue)).start()
                    message = result_queue.get()

                    threading.Thread(target=delete_data, args=(data,)).start()

                    return jsonify({
                        "message": "Data inserted into the audit report",
                        "delete_message": "Application deleted successfully.",
                        "auditor_id": aud_id,
                        "phone": row['phone'],
                        "auditor_name": row['auditor_name'],
                        "audit_message": message,
                    }), 200

                else:
                    # For rejected applications
                    query = "DELETE FROM applications WHERE status = %s"
                    pointer.execute(query, (state,))
                    conn.commit()
                    print('Application with status %s deleted successfully' % state)
                    return jsonify({"message": "Application rejected."}), 200

    except Exception as e:
        print("The error was:", str(e))
        return jsonify({"error": str(e)}), 500

def clean_date(date_str):
    try:
        # Parse the RFC1123 format
        parsed_date = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %Z')
        print(parsed_date)

        # MySQL doesn't support years below 1000
        if parsed_date.year < 1000:
            # You can either reject, return None, or set a default
            return None  # or return a fallback like: return '2000-01-01 00:00:00'

        # Convert to MySQL-friendly format
        return parsed_date.strftime('%Y-%m-%d %H:%M:%S')

    except Exception as e:
        print(f"Date parsing error: {e}")
        return None



# location info
def loca(value):
    try:
        print('the audit is is ',value)
        #query to search in the table
        location_query="""select loction from audit_details where Audit_id=%s"""
        # getting connection to the db
        with get_connection() as conn:
            pointer = conn.cursor(dictionary=True)
            pointer.execute(location_query,(value,))
            location_info=pointer.fetchone()
            print(location_info)

        return location_info

    except Exception as e:
        print(f"Date parsing error: {e}")
        return None

def delete_data(data):
    try:
        time.sleep(10)
        print('the data',data)
        status=[]
        for row in data:
            details=row['status']
            print('details')
            status.append(details)
        print(status)
        value=status[0]

        # search query for db
        query="""delete from applications where status=%s"""
        with get_connection() as conn:
            pointer = conn.cursor(dictionary=True)
            pointer.execute(query ,(value,))
            print('data deleted successfully')
    except Exception as e:
        print(str(e))


# for generating auditor_id
def auditor_id():
    with get_connection() as conn:
        pointer = conn.cursor(dictionary=True)
        pointer.execute("SELECT auditor_id FROM audit_report ORDER BY auditor_id DESC LIMIT 1")
        result=pointer.fetchone()
        print(result)
        if result:
            print('at auditor id')
            last_id = result['auditor_id']  # e.g., "AUD023"
            numeric_part = int(last_id[3:])  # Extract numeric part after "AUD"
            next_numeric = numeric_part + 1
            new_id = f"AUD{next_numeric:03d}"
        else:
            next_numeric = 1  # Start from 1 if table is empty
            new_id = f"AUD{next_numeric:03d}"

    return new_id


def delete_audit_data(Audit_id,result_queue):
    try:
        time.sleep(8)
        query="""select Auditors_require from audit_details where Audit_id=%s"""
        audit_id=Audit_id[0]['audit_id']
        with get_connection() as conn:
            pointer = conn.cursor(dictionary=True)
            pointer.execute(query,(audit_id,))
            data = pointer.fetchall()
            print(data)
            data1=data[0]
            auditors=data1['Auditors_require']
        if auditors==1:
            # when the require auditor is one then the audit is deleted from db else

            delete_query="""delete from audit_details where Audit_id=%s"""
            with get_connection() as conn:
                pointer = conn.cursor(dictionary=True)
                pointer.execute(delete_query, (audit_id,))
                print('the audit data is deleted')
            if audit_id:
                delete_application="""delete from applications where Audit_id=%s"""
                with get_connection() as conn:
                    pointer = conn.cursor(dictionary=True)
                    pointer.execute(delete_application, (audit_id,))
                    print('the applications deleted data is deleted')
            result_queue.put("Audit is Delete Successful")

        else:

            #if the auditor require more then one then the requirement is updated accordingly..

            update_query="""update audit_details set Auditors_require=%s where Audit_id=%s"""

            new_auditors=int(auditors)-1
            with get_connection() as conn:
                pointer = conn.cursor(dictionary=True)
                pointer.execute(update_query, (new_auditors,audit_id))
            result_queue.put("Auditor requirement Update Successful")
    except Exception as e:
        print( 'the delete error is ',str(e))
        return jsonify(str(e))


@application.route('/admin/application/filter' ,methods=['POST','GET'])
def fliter_Application():
    try:
        data=request.get_json()
        print(data)
        input=data['searchInput']
        status=data['selection']


        if status=="name":
            name=f'%{input}%'
            print(name)
            query="""select * from applications where auditor_name like %s"""
            with get_connection() as conn:
                pointer = conn.cursor(dictionary=True)
                pointer.execute(query ,(name,))
                data=pointer.fetchall()
                print('the filterd',data)
            return jsonify(data)
        elif status=="audit_type":
            query = """select * from applications where Audit_id=%s"""
            with get_connection() as conn:
                pointer = conn.cursor(dictionary=True)
                pointer.execute(query ,(input,))
                audit_data=pointer.fetchall()
                print('the filterd',audit_data)
            return jsonify(audit_data)
        elif status=="email":
            email=input
            query = """select * from applications where email=%s"""
            with get_connection() as conn:
                pointer = conn.cursor(dictionary=True)
                pointer.execute(query ,(email,))
                email_filter=pointer.fetchall()
                print('the filterd',email_filter)
            return jsonify(email_filter)
        else:
            print('select the filter')
            return jsonify('select the correct fileld')

    except Exception as e:
        return jsonify(e), 500





















