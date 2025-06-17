from flask import Flask, redirect, Blueprint,request,jsonify
from datetime import datetime
from audit_tarcker.config import get_connection

audit_log=Blueprint('audit_log' ,__name__)


# single record update in the database
@audit_log.route('/admin/manual_update' ,methods=['POST'])
def manual_update():
    json_data=request.get_json()
    print(json_data)
    if json_data=='':
        print('no data received')
    data=json_data['data']
    try:
        date_str = data["Date"]

        # Detect the format and parse accordingly
        if "-" in date_str:  # Example: 2025-03-20 (YYYY-MM-DD)
           date = date_str  # Already correct, no conversion needed
        else:  # Example: 03/20/25 (MM/DD/YY)
            date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")

        # Store the planned_date
        data["Date"]= date

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    try:
        query="""insert into audit_details(
                Audit_id,
                Audit_type,
                industry,
                Date,
                Auditors_require,
                Days,
                Qualification,
                equipment,
                loction,
                state,
                Amount,
                Client_id,
                WhatsappLink
            ) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        with get_connection() as conn:
            pointer = conn.cursor(dictionary=True)
            pointer.execute(query, ( data['Audit Id'],data['Audit type'] ,data['industry'],data['Date'],data['auditor require'],data['Days'],data['Qualification'],data['equipment'],data['location'],data['State'],data['Amount'],data['client_id'] ,data['whatsapp']))
        print('new audit data is  inserted in the database through admin ')
        return jsonify('data inserted successfully...')
    except Exception as e:
        print(e)
        return jsonify(str(e)) ,400

# audit details card

@audit_log.route("/audit_details")
def audit_details():
    try:
        query="""select * from audit_details """
        with get_connection() as conn:
            pointer = conn.cursor(dictionary=True)
            pointer.execute(query)
            data=pointer.fetchall()
            print(data)

        return jsonify(data)
    except Exception as e:
        print(e)
        return jsonify(e),400

@audit_log.route("/home_page/audits")
def home_page_audit_details():
    try:
        query="""select * from audit_details limit 5 """
        with get_connection() as conn:
            pointer = conn.cursor(dictionary=True)
            pointer.execute(query)
            data=pointer.fetchall()
            print(data)
        return jsonify(data)
    except Exception as e:
        print(e)
        return jsonify(e),400

@audit_log.route('/admin/delete_out_dated_audit',methods=["POST","GET"])
def out_dated_audits():
    try:
        data = request.get_json()
        print(data)
        delete_date=data['date']
        incoming_date = datetime.strptime(delete_date, "%a, %d %b %Y %H:%M:%S %Z").date()
        print(incoming_date)

        query="""delete from audit_details where Date=%s"""
        with get_connection() as conn:
            pointer = conn.cursor(dictionary=True)
            pointer.execute(query,(incoming_date,))

            print('audit data deleted...')

        return jsonify({'message':'Out Dated Audits are deleted'})
    except Exception as e:
        print(str(e))






