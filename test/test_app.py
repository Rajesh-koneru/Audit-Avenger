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

def test_home_page(client):
    """Test if the home page loads correctly"""
    response = client.get('/admin/Recent_audit')
    assert response.status_code == 200

    # Parse JSON response
    data = json.loads(response.data)

    # Check if expected data is present (modify based on actual data structure)
    assert isinstance(data, list)  # Ensure response is a lis
"""def test_update_route(client):
    # testing update route

    data={"Id":"AA0001","value":" "}
    response = client.post('/admin/update_status',json=data)

    # Verify that the status code is 200.
    assert response.status_code == 200

    # Verify the response JSON.
    response_json = response.get_json()
    assert response_json["message"] == "database updated successfully..."
"""
def test_upload(client):
    response=client.get("/auditor/auditor_details")
    assert response.status_code == 200

    # Parse JSON response
    data = json.loads(response.data)

    # Check if expected data is present (modify based on actual data structure)
    assert isinstance(data, list)  # Ensure response is a list


