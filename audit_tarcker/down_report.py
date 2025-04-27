from flask import Blueprint, request, send_file
import pandas as pd
import io
from flask_login import login_required
from audit_tarcker.test import only_one
from audit_tarcker.config import get_connection

# Define the Blueprint
download = Blueprint('file_download', __name__)

@download.route('/admin/download', methods=["POST"])
@login_required
@only_one('admin')
def file_download():
    req = request.get_json()
    name = req.get('fileName', 'audit_report')  # Default filename if not provided

    def fetch_data():
        download_query = "SELECT * FROM audit_report"
        conn = get_connection()  # Get connection
        try:
            with conn.cursor() as cursor:
                cursor.execute(download_query)
                data = cursor.fetchall()
                df = pd.DataFrame(data)  # Convert to DataFrame
            return df
        finally:
            conn.close()  # Ensure connection is closed

    # Fetch data
    dframe = fetch_data()

    # Check if data exists
    if dframe.empty:
        return {"message": "No data available to download"}, 404

    # Save file to in-memory buffer
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        dframe.to_excel(writer, index=False, sheet_name='Sheet1')

    output.seek(0)  # Reset buffer pointer
    print('file downloaded...')
    # Send file as response
    return send_file(output,
                     download_name=f"{name}.xlsx",
                     as_attachment=True,
                     mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
