from flask import Blueprint, request, jsonify
from flask_mail import Message
from audit_tarcker.mail_config import mail, email

mail_bp = Blueprint('mail', __name__)

@mail_bp.route('/sendMail', methods=['POST'])
def send_email():
    data = request.json
    name = data.get('SenderName')
    email1 = data.get('Email')
    message_body = data.get('Message')
    import os

    if not name or not email or not message_body:
        return jsonify({'error': 'All fields are required!'}), 400

    msg = Message(
        subject=f"New Contact Form Submission from {name}",
        recipients=[os.getenv('MAIL_USERNAME')],  # Your email to receive the message
        body=f"Name: {name}\nEmail: {email1}\nMessage: {message_body}"
    )

    try:
        mail.send(msg)
        return jsonify({'message': 'Email sent successfully!'}), 200
    except Exception as e:
        return jsonify({'error': f'Failed to send email: {str(e)}'}), 500
