from flask import Flask, Blueprint, redirect, request, jsonify, render_template
from audit_tarcker.config import get_connection

register=Blueprint('signin' ,__name__)
@register.route('/registration',methods=['POST'])
def signin():
    json_data = request.get_json()
    print(json_data)
    if json_data == '':
        print('no data received')

    def auditor_id():
        with get_connection() as conn:
            pointer = conn.cursor()
            pointer.execute("SELECT auditor_id FROM auditor_details ORDER BY auditor_id DESC LIMIT 1")
            result=pointer.fetchone()
            print(result)
            if result:
                last_id = result['auditor_id']  # e.g., "AUD023"
                numeric_part = int(last_id[3:])  # Extract numeric part after "AUD"
                next_numeric = numeric_part + 1
                new_id = f"AUD{next_numeric:03d}"

            else:
                next_numeric = 1  # Start from 1 if table is empty
                new_id = f"AUD{next_numeric:03d}"

        return new_id
    aud_id=auditor_id()
    print(aud_id)

    try:
        query="""insert into auditor_details(
                Auditor_id,
                Auditor_name,
                contact,
                email,
                password,
                Qualification,
                experience
            ) values(%s,%s,%s,%s,%s,%s,%s)"""
        with get_connection() as conn:
            pointer = conn.cursor()
            pointer.execute(query, (aud_id,json_data['name'],json_data['phone'] ,json_data['email'],json_data['password'],json_data['qualification'],json_data['experience']))
        return jsonify({'message':'data inserted successfully...'})
    except Exception as e:
        print(e)
        return jsonify(e) ,400
