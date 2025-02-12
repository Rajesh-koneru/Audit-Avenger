from flask import Flask, render_template,jsonify,redirect
from secrets import token_hex

from flask_login import login_required
from flask_session import Session
from index import  login_manager
from AdminReport import report
from index import auth
from auditor_stauts import audit_status
from upolad import file

app = Flask(__name__)

# Flask-Login setup
login_manager.login_view = "auth.login"
login_manager.init_app(app)


app.secret_key = 'hello i am hacker'
app.secret_key = token_hex(16)  # Secure session key
app.config['SESSION_TYPE'] = 'filesystem'  # You can also use Redis, MongoDB, etc.
Session(app)

# auth blueprint registration
app.register_blueprint(auth)

# report blueprint
app.register_blueprint(report)

# auditor_stauts blueprint
app.register_blueprint(audit_status)



#file upload blueprint registration
app.register_blueprint(file)
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
@app.route('/dashboard') # Role-based check first
@login_required  # Then login check
def dashboard():
    return render_template('dashboard.html')


@app.route('/auditor')
def status():
    return render_template('admin.html')


@app.route('/report')
def repo():
    return render_template('report1.html')


@app.route('/upload')
def upload():
    return render_template('fileUpload.html')
if __name__ == '__main__':
    app.run(debug=True)



