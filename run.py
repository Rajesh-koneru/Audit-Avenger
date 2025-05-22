from audit_tarcker import create_App
from flask_cors import CORS
import os
app = create_App()
CORS(app,supports_credentials=True)
if __name__ == '__main__':
     # Use Render’s assigned port
    app.run(host="127.0.0.1", port=5000, debug=True)
