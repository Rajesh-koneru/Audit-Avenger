from flask import Flask
from flask_mail import Mail
import os
mail= Flask(__name__)

# Flask-Mail Configuration
mail.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Use Gmail SMTP
mail.config['MAIL_PORT'] = 587
mail.config['MAIL_USE_TLS'] = True
mail.config['MAIL_USERNAME'] =  os.getenv('MAIL_USERNAME')  # Replace with your email
mail.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')  # Use App Password, not Gmail password
mail.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')

email = Mail(mail)
