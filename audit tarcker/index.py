from flask import Flask, Blueprint, request, session, redirect, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
import os

# Securely store admin credentials (Better to use environment variables)
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'Admin@raghu')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'Raghu@1234')


# Auth blueprint
auth = Blueprint('auth', __name__)

# Flask-Login setup
login_manager = LoginManager()
# User Model for Admin Only
class Admin(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    if user_id == "admin":
        return Admin(id="admin")
    return None

# Admin login route
@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        # Only allow the admin to log in
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            user = Admin(id="admin")
            session['username'] = username
            session['islogin'] = True
            login_user(user)
            return redirect('/admin1')
        else:
            return "Unauthorized", 401

    return redirect('/login_page')

# Logout route
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect('/')

# Admin dashboard route (restricted to admin only)
@auth.route('/admin1')
@login_required
def admin():
    if session.get('username') == ADMIN_USERNAME:
        return redirect('/dashboard')
    return "Unauthorized", 403


