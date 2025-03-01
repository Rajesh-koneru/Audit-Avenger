import psycopg2
import os
# Manually set the values from Render Dashboard
DATABASE_URL=os.getenv( "database_url","postgresql://audit_tracker_user:IQbR3YNHshKyIN0a9S5BYgWHuAdbHx4S@dpg-cv0uku3tq21c73esj0ng-a/audit_tracker")


# sql lite database
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Get the directory of the current file
AuditTrack = os.path.join(BASE_DIR, '..', 'instance', 'auditTracker.db')

