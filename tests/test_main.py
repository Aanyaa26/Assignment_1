import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_address():
    payload = {
        "address": {
            "hn": 10,
            "ap": "Test Apartments",
            "pincode": 110001
        }
    }

    response = client.post("/address", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert data["message"] == "Address saved successfully"
    assert data["data"]["hn"] == 10

def test_invalid_pincode():
    payload = {
        "address": {
            "hn": 10,
            "ap": "Test",
            "pincode": 123
        }
    }

    response = client.post("/address", json=payload)

    assert response.status_code == 422

def test_invalid_pincode():
    payload = {
        "address": {
            "hn": 10,
            "ap": "Test",
            "pincode": 123
        }
    }

    response = client.post("/address", json=payload)

    assert response.status_code == 422

def test_wrong_type():
    payload = {
        "address": {
            "hn": "abc",
            "ap": "Test",
            "pincode": 110001
        }
    }

    response = client.post("/address", json=payload)

    assert response.status_code == 422


