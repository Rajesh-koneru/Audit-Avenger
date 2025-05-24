from flask import Flask, Blueprint, redirect, session, request, jsonify, url_for, render_template
from audit_tarcker.config import get_connection

audit_bp = Blueprint('apply', __name__)


@audit_bp.route('/apply/user_Details' ,methods=['POST','GET'])
def register_page():
    if request.method == 'POST':
        data = request.get_json()
        info=data['data']
        print(info)
        print('the received data ',data)
        audit_id = info.get('audit_id')
        whatsapp_link=info.get('whatsappLink')
        session['whatsappLink']=whatsapp_link
        session["Audit_id"] = audit_id
        return jsonify({'message': 'Audit ID stored in session'})
    return render_template('registration.html')


@audit_bp.route('/apply/audit_application', methods=['POST',"GET"])
def application():
    print('entering into application...')
    # Check login
    audit_id = session.get('Audit_id')
    print(audit_id)
    if not audit_id:
        return jsonify({'error': 'Session expired or audit ID not set'}), 403

    json_data = request.get_json()
    print(json_data)
    if not audit_id:
        return jsonify({'error': 'Missing audit_id'}), 400

    def auditor_id():
        with get_connection() as conn:
            pointer = conn.cursor(dictionary=True)
            pointer.execute("SELECT Auditor_id FROM applications ORDER BY Auditor_id DESC LIMIT 1")
            result=pointer.fetchone()
            print(result)
            if result:
                print('at auditor id')
                last_id = result['Auditor_id']  # e.g., "AUD023"
                numeric_part = int(last_id[3:])  # Extract numeric part after "AUD"
                next_numeric = numeric_part + 1
                new_id = f"AUD{next_numeric:03d}"
            else:
                next_numeric = 1  # Start from 1 if table is empty
                new_id = f"AUD{next_numeric:03d}"

        return new_id


    def get_audit_data():
        try:
            Audit_id = session.get('Audit_id')
            print("The audit id for retrieving data:", Audit_id)

            if not Audit_id:
                raise ValueError("Audit_id not found in session")

            query = """
                SELECT Audit_id, Audit_type, Date, Client_id, state 
                FROM audit_details 
                WHERE Audit_id = %s
            """
            with get_connection() as conn:
                pointer = conn.cursor(dictionary=True)
                pointer.execute(query, (Audit_id,))
                result = pointer.fetchone()
                if not result:
                    raise ValueError(f"No audit found with Audit_id: {Audit_id}")
                return result
        except Exception as e:
            print("Error in get_audit_data:", str(e))
            return None

    def insert_application(json_data, audit_data):
        try:
            print("Inserting audit data...")
            aud_id = auditor_id()
            insert_query = """
                INSERT INTO applications 
                (Auditor_id, auditor_name, phone, email, audit_id, audit_type, date, client_id, state) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            with get_connection() as conn:
                pointer = conn.cursor(dictionary=True)
                pointer.execute(insert_query, (
                    aud_id,
                    json_data['name'], json_data['phone'], json_data['email'],
                    audit_data['Audit_id'], audit_data['Audit_type'], audit_data['Date'],
                    audit_data['Client_id'], audit_data['state']
                ))
                conn.commit()
                print("Data inserted successfully.")
            return jsonify({
                'message': 'Your Application is saved Successfully.',
                'link': session.get('whatsappLink', '')
            }), 200

        except Exception as e:
            print("Unexpected error in insert_application:", str(e))
            return jsonify({'error': 'Unexpected server error.', 'details': str(e)}), 500

    # Main logic (likely inside your route)
    audit_data = get_audit_data()
    if not audit_data:
        return jsonify({'error': 'Audit data not found or session expired.'}), 400

    return insert_application(json_data, audit_data)
