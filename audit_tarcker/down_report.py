from flask import blueprints, request, send_file, Blueprint
import pandas as pd
import io
import sqlite3
import os
from pymysql import connect
from flask_login import login_required
from audit_tarcker.test import only_one
from audit_tarcker.config import collection



# download a file from app
download = Blueprint('file_download', __name__)
#BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Get the directory of the current file
#AuditTrack = os.path.join(BASE_DIR, '..', 'instance', 'auditTracker.db')
@download.route('/admin/download', methods=["POST"])
@login_required
@only_one('admin')

def file_download():
    req=request.get_json()
    name=req.get('fileName')
    if name:
        print(name)
    def fetch_data():
        data=list(collection.find({},{"_id":0}))
        df = pd.DataFrame(data)
        return df
    dframe=fetch_data()
   # save file to in memory file
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        dframe.to_excel(writer, index=False, sheet_name='Sheet1')

    output.seek(0)  # Move to the start of the file
# send file AS reponse
    print("file downloaded")
    return send_file(output, download_name=f"{name}.xlsx", as_attachment=True,mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
