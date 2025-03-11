from flask import Blueprint, request, jsonify
from flask_mail import Message
import os
import smtplib
from audit_tarcker.mail_config import mail

mail_bp = Blueprint('mail', __name__)

@mail_bp.route('/sendMail', methods=['POST'])
def send_email():
    data = request.json
    name = data.get('SenderName')
    email1 = data.get('Email')  # Changed to avoid conflict
    message_body = data.get('Message')
    print(message_body)

    if not name or not email1 or not message_body:
        return jsonify({'error': 'All fields are required!'}), 400

    recipient_email = os.getenv('MAIL_USERNAME')
    if not recipient_email:
        return jsonify({'error': 'Recipient email is not configured'}), 500

    msg = Message(
        subject=f"New Contact Form Submission from {name}",
        recipients=[recipient_email],
        body=f"Name: {name}\nEmail: {email1}\nMessage: {message_body}"
    )

    print(msg)
    try:
        mail.send(msg)
        print('mail sends successfully')
        return jsonify({'message': 'Email sent successfully!'}), 200
    except smtplib.SMTPAuthenticationError:
        return jsonify({'error': 'Invalid SMTP credentials'}), 500
    except smtplib.SMTPConnectError:
        return jsonify({'error': 'Failed to connect to SMTP server'}), 500
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

