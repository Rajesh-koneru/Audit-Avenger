from flask import Blueprint, render_template, jsonify
from flask_login import login_required
import sqlite3

from werkzeug.utils import redirect

from test import only_one

db1 = Blueprint('admin_db', __name__ ,url_prefix='/admin')  # Correct blueprint initialization
@db1.route('/admin')
@login_required
@only_one('admin')
def admin_access():
    """
    Route to access admin page. Fetches audit details from the database and renders them.
    """
    query = '''SELECT * FROM Audit_details'''
    try:
        with sqlite3.connect('auditTracker.db') as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            return render_template('dashboard.html')
    except sqlite3.OperationalError as e:
        return f"Database Error: {e}"

@db1.route('/profile')
@login_required
def prof():
    """
    Route to view a sample profile.
    """
    return "Your profile is name: Raju, age: 20, branch: ECE"

