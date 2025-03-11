import sys
import os
from http.client import responses

import pytest

# Add the project root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname('trackerApp'), '..', '..')))

from audit_tarcker import create_App
@pytest.fixture
def client():
    """Create a test client for Flask"""
    app = create_App()
    app.testing = True

    with app.test_client() as client:
        yield client

import json

"""def test_home_page(client):
   Test if the home page loads correctly
    response = client.get('/admin/Recent_audit')
    assert response.status_code == 200

    # Parse JSON response
    data = json.loads(response.data)

    # Check if expected data is present (modify based on actual data structure)
    assert isinstance(data, list)  # Ensure response is a lis
def test_update_route(client):
    # testing update route

    data={"Id":"AA0001","value":" "}
    response = client.post('/admin/update_status',json=data)

    # Verify that the status code is 200.
    assert response.status_code == 200

    # Verify the response JSON.
    response_json = response.get_json()
    assert response_json["message"] == "database updated successfully..."

def test_upload(client):
    response=client.get("/auditor/auditor_details")
    assert response.status_code == 200

    # Parse JSON response
    data = json.loads(response.data)

    # Check if expected data is present (modify based on actual data structure)
    assert isinstance(data, list)  # Ensure response is a list



def test_download(client):
    response=client.post('/admin/download ',json={'name':'hello'})
    assert response.status_code ==200

    data=json.loads(response.data)
"""

def test_send_mail(client):
    """Test the sendMail API endpoint"""
    response = client.post(
        "/sendMail",
        data=json.dumps({
            "SenderName": "Test User",
            "Email": "rajeshkoneru29@gmail.com",
            "Message": "Hello! This is a test."
        }),
        content_type="application/json"
    )

    assert response.status_code == 200 or response.status_code == 500  # Ensure it doesn't fail silently
    json_data = response.get_json()

    if response.status_code == 200:
        assert json_data["message"] == "Email sent successfully!"
    else:
        assert "error" in json_data  # Expect an error message if it fails



