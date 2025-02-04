from flask import Flask, render_template,jsonify,redirect
from flask_login import LoginManager, login_user, logout_user, current_user, login_required, UserMixin
from test import only_one
from flask_session import Session
from index import get_user_by_username , load_user,login,logout,sigin,Users,login_manager
from AdminReport import report
from index import auth
from auditor_stauts import audit_status
# Initialize the login manager
app = Flask(__name__)
login_manager.init_app(app) # Redirect unauthorized users to login page
# session
#Configuring SQLAlchemy and Flask-Session
# Initialize the Flask-Session extension
app.secret_key = 'hello i am hacker'
app.config['SESSION_TYPE'] = 'filesystem'  # You can also use Redis, MongoDB, etc.
Session(app)

# auth blueprint registration
app.register_blueprint(auth)

# report blueprint
app.register_blueprint(report)

# auditor_stauts blueprint
app.register_blueprint(audit_status)
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

# report route
@app.route('/admin/report')
def admin_report():

    return redirect('/admin/report')
# Dashboard (Protected)
@app.route('/dashboard')
@only_one('admin')  # Role-based check first
@login_required  # Then login check
def dashboard():
    return render_template('dashboard.html')
@app.route('/auditor')
def status():
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True)



