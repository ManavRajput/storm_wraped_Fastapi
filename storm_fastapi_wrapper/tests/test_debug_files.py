from fastapi.testclient import TestClient
from storm_fastapi_wrapper.main import app

client = TestClient(app)

def test_debug_files_should_be_empty():
    response = client.get("/debug/files")
    assert response.status_code == 200
    assert response.json() == {}  # Should be empty if no file writes
