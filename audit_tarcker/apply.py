# application routes for audit assignment

from flask import Flask ,Blueprint,redirect ,session,request,jsonify
from audit_tarcker.config import get_connection
import urllib.parse
audit=Blueprint('apply',__name__)

@audit.route('/audit_application')
def application():
    user=session['username']
    id=session['id']
    data = request.get_json()
    #extracting user dat from auditor details table
    def user_Data():
        auditor="""select Auditor_name,phone,email from auditor_details Auditor_name=%s and password=%s"""
        with get_connection() as conn:
            pointer = conn.cursor()
            pointer.execute(auditor,(user,id))
            user_data = pointer.fetchone()
            print(user_data)
        return user_data
    #extracting audit details from audit table...
    def audit():
        audit_data="""select Audit_id,audit_type, Date, client_id f+rom audit_details where Audit_id=%s"""
        with get_connection() as conn:
            pointer = conn.cursor()
            pointer.execute(audit_data, (data,))
            audit_data = pointer.fetchone()
            print(audit_data)
        return audit_data
    def applications():
        try:
            user_data=user_Data()
            audit_data=audit()
            application="""insert into applications values(%s ,%s,%s,%s,%s,%s,%s)"""
            with get_connection() as conn:
                pointer=conn.cursor()
                pointer.execute(application,(user_data['auditor_name'],user_data['phone'],user_data['email'],audit_data['Audit_id'],audit_data['audit_type'],audit_data['Date'],audit_data['client_id']))
                print('data inserted successfully...')
        finally:
            conn.commit()
            pointer.close()
    applications()
    print('application saved successfully')
    audit_id=audit()
    # WhatsApp message
    message = f"Hi, I'm applying for Audit #{audit_id['Audit_id']}. Please let me know the payment details."
    encoded_msg = urllib.parse.quote(message)

    # Redirect to WhatsApp
    whatsapp_url = f"https://wa.me/9390193971?text={encoded_msg}"
    return redirect(whatsapp_url)


