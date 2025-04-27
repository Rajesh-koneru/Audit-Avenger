# test_app.py
import pytest
from unittest.mock import patch, MagicMock
from flask import session
from audit_tarcker import create_App

flask_app = create_App()

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    flask_app.secret_key = 'test_secret'
    with flask_app.test_client() as client:
        with client.session_transaction() as sess:
            sess['username'] = 'testuser'
            sess['id'] = 1
        yield client

# PATCH WHERE request AND get_connection ARE USED (in apply.py)
@patch('audit_tarcker.apply.get_connection')
@patch('audit_tarcker.apply.request')
def test_application_redirects_to_whatsapp(mock_request, mock_get_conn, client):
    # Mock incoming JSON data
    mock_request.get_json.return_value = 123  # audit_id

    # Mock DB connection and cursor behavior
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_conn.return_value.__enter__.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    # Setup fetchone side_effect (user_data, then audit_data)
    mock_cursor.fetchone.side_effect = [
        {'auditor_name': 'John Doe', 'phone': '9999999999', 'email': 'john@example.com'},
        {'Audit_id': 123, 'audit_type': 'Financial', 'Date': '2025-04-16', 'client_id': 321}
    ]

    # Make POST request
    response = client.post('/application')

    # Assert redirect
    assert response.status_code == 302
    assert "https://wa.me/9390193971?text=" in response.location
    assert "Audit%20%23123" in response.location
