from flask import Flask, Blueprint

# Create a Blueprint with a URL prefix
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Define routes within the Blueprint
@admin_bp.route('/')
def admin_home():
    return "Welcome to the Admin Dashboard"

@admin_bp.route('/users')
def manage_users():
    return "Manage Users Page"

@admin_bp.route('/settings')
def admin_settings():
    return "Admin Settings Page"

# Create the main Flask app
app = Flask(__name__)

# Register the Blueprint with the app
app.register_blueprint(admin_bp)

# Define a route in the main app
@app.route('/')
def home():
    return "Welcome to the Main App"

if __name__ == '__main__':
    app.run(debug=True)
