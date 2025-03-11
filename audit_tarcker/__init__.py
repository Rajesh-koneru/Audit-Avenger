from flask import Flask, render_template, jsonify, redirect
from secrets import token_hex
from pymongo import MongoClient
import os
from flask_login import login_required
from flask_session import Session
from audit_tarcker.mail_config import mail

# database connection
#BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'instance'))
#AuditTrack = os.path.join(BASE_DIR, 'auditTracker.db')

def create_App():
    from audit_tarcker.index import login_manager
    from audit_tarcker.auditor_page import status
    from audit_tarcker.AdminReport import report
    from audit_tarcker.index import auth
    from audit_tarcker.config import collection
    from audit_tarcker.upolad import file
    from audit_tarcker.down_report import download
    from audit_tarcker.test import only_one
    from audit_tarcker.database import mango_base
    from audit_tarcker.Smtp import mail_bp


    app = Flask(__name__)
    app.config["MONGO_URI"] = "mongodb+srv://raghavendhargpth:MLOBWMCnt6VD9dkh@cluster0.9ipen.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

    # ✅ Connect to MongoDB
    mongo_client = MongoClient(app.config["MONGO_URI"])

    app.mongo_client = mongo_client
    app.audit_collection =collection

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

    #registering mail server
    app.register_blueprint(mail_bp)

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
        return render_template('newaudit.html')
    return app
