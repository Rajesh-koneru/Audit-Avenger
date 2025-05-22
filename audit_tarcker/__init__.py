from flask import Flask, render_template, jsonify, redirect
from secrets import token_hex
import os
from flask_login import login_required
from flask_session import Session
from grpclib.plugin.main import render

from audit_tarcker.mail_config import mail


# database connection
#BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'instance'))
#AuditTrack = os.path.join(BASE_DIR, 'auditTracker.db')

def create_App():
    from audit_tarcker.index import login_manager
    from audit_tarcker.auditor_page import status
    from audit_tarcker.AdminReport import report
    from audit_tarcker.index import auth
    from audit_tarcker.config import get_connection
    from audit_tarcker.upolad import file
    from audit_tarcker.down_report import download
    from audit_tarcker.test import only_one
    from audit_tarcker.database import mango_base
    from audit_tarcker.Smtp import mail_bp
    from audit_tarcker.Audit_log import audit_log
    from audit_tarcker.register import register
    from audit_tarcker.apply import audit_bp
    from audit_tarcker.whatsappweb import application

    app = Flask(__name__)
    # ✅ Connect to MongoDB


    """app.mongo_client = mongo_client
    app.audit_collection =collection
"""
    # Flask-Login setup
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)


    # mail server configuration

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Use Gmail SMTP
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')  # Replace with your email
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')  # Use App Password, not Gmail password
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')

    # Initialize mail with app
    mail.init_app(app)

    app.secret_key = token_hex(16)  # Secure session key
    app.config['SESSION_TYPE'] = 'filesystem'
    Session(app)

    # Register Blueprints (Ensuring Unique Names)
    app.register_blueprint(auth)
    app.register_blueprint(report)
    app.register_blueprint(file)
    app.register_blueprint(status, name="status_blueprint")  # ✅ Unique name
    app.register_blueprint(download)
    app.register_blueprint(mango_base)
    app.register_blueprint(audit_log)


    #registering mail server
    app.register_blueprint(mail_bp)


   # register blueprint
    app.register_blueprint(register)


    #application register
    app.register_blueprint(audit_bp)

    # application blueprint
    app.register_blueprint(application)


    @app.route('/')
    def home():
        return render_template('home1.html')

    # Signup Page
    @app.route('/signup_page')
    def signup():
        return render_template('sinin.html')


    # Admin report
    @app.route('/admin/report')
    def admin_report():
        return redirect('/admin/report')

    # Dashboard (Protected)
    @app.route('/admin/dashboard')  # Role-based check first
    @login_required  # Then login check
    @only_one('admin')
    def dashboard():
        return render_template('dashboard.html')

    @app.route('/report')
    def repo():
        return render_template('report2.html')

    @app.route('/admin/manual_data')
    def new_data():
        return render_template('1.html')

    @app.route('/application')
    def application():
        return render_template('application.html')

    @app.route('/audit_card',methods=['GET'])
    def card():
        return render_template('audit card .html')
    return app
