from flask import Flask, render_template, jsonify, redirect
from secrets import token_hex
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import login_required
from flask_session import Session

# database connection
db = SQLAlchemy()
app=Flask(__name__)
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


    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI']=collection
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    # Flask-Login setup
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    app.secret_key = token_hex(16)  # Secure session key
    app.config['SESSION_TYPE'] = 'filesystem'
    Session(app)

    # Register Blueprints (Ensuring Unique Names)
    app.register_blueprint(auth)
    app.register_blueprint(report)
    app.register_blueprint(file)
    app.register_blueprint(status, name="status_blueprint")  # ✅ Unique name
    app.register_blueprint(download)


    @app.route('/')
    def home():
        return render_template('home1.html')

    # Signup Page
    @app.route('/signup_page')
    def signup():
        return render_template('sinin.html')

    # Sign-in Page
    @app.route('/signin_page')
    def signin():
        return render_template('register.html')

    # Admin report
    @app.route('/admin/report')
    def admin_report():
        return redirect('/admin/report')

    # Dashboard (Protected)
    @app.route('/dashboard')  # Role-based check first
    @login_required  # Then login check
    def dashboard():
        return render_template('dashboard.html')

    @app.route('/auditor_page')  # Renamed to avoid conflict with blueprint
    def auditor_page():
        return render_template('admin.html')

    @app.route('/report')
    def repo():
        return render_template('report1.html')
    return app
