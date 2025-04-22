import pytest
from fastapi.testclient import TestClient
from storm_fastapi_wrapper.main import app

client = TestClient(app)

def test_successful_query_response():
    payload = {
        "query": "How does photosynthesis work?",
        "stream": False,
        "temperature": 0.7
    }
    response = client.post("/query", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["output"] and isinstance(data["output"], str)

def test_empty_query_rejected():
    payload = {
        "query": "   ",
        "stream": False,
        "temperature": 0.7
    }
    response = client.post("/query", json=payload)
    assert response.status_code == 422  # Validation error

def test_temperature_bounds():
    payload = {
        "query": "What is AI?",
        "stream": False,
        "temperature": 2.5  # Invalid
    }
    response = client.post("/query", json=payload)
    assert response.status_code == 422
