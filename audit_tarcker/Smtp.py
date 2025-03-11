from flask import Blueprint, request, jsonify
from flask_mail import Message
import os
import smtplib
from audit_tarcker.mail_config import mail
import traceback
mail_bp = Blueprint('mail', __name__)

@mail_bp.route('/sendMail', methods=['POST'])


@mail_bp.route('/sendMail', methods=['POST'])
def send_email():
    data = request.json
    print("🚀 Received request:", data)  # Debugging

    name = data.get('SenderName')
    email1 = data.get('Email')  # Changed to avoid conflict
    message_body = data.get('Message')
    print("📩 Message Content:", message_body)

    if not name or not email1 or not message_body:
        print("🛑 Validation failed: Missing fields")  # Debugging
        return jsonify({'error': 'All fields are required!'}), 400

    recipient_email = os.getenv('MAIL_USERNAME')
    if not recipient_email:
        print("⚠️ Missing environment variable: MAIL_USERNAME")  # Debugging
        return jsonify({'error': 'Recipient email is not configured'}), 500

    msg = Message(
        subject=f"New Contact Form Submission from {name}",
        recipients=[recipient_email],
        body=f"Name: {name}\nEmail: {email1}\nMessage: {message_body}"
    )

    print("📨 Message Object:", msg)

    try:
        mail.send(msg)
        print('✅ Mail sent successfully!')
        return jsonify({'message': 'Email sent successfully!'}), 200
    except Exception as e:
        print("❌ Error sending email:")
        traceback.print_exc()  # Prints full error details
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500
