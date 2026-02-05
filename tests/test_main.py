import sys
import os
from unittest.mock import MagicMock

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from fastapi.testclient import TestClient
from main import app, get_db

# ---- MOCK DATABASE ----
def override_get_db():
    db = MagicMock()
    yield db

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# ---- TESTS ----

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


def test_missing_field():
    payload = {
        "address": {
            "hn": 10
        }
    }

    response = client.post("/address", json=payload)
    assert response.status_code == 422
