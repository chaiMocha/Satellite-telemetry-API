from fastapi.testclient import TestClient
from main import app
from datetime import datetime, timezone

client = TestClient(app)

def test_ingest_telemetry():
    payload = {
        "satellite_id": "SAT-Alpha-1",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "battery_level": 94.5,
        "latitude": 35.123,
        "longitude": -100.456,
        "altitude": 400.5
    }
    response = client.post("/telemetry/", json=payload)
    assert response.status_code == 201
    assert response.json()["satellite_id"] == "SAT-Alpha-1"
    assert "id" in response.json()

def test_get_latest_telemetry():
    response = client.get("/telemetry/SAT-Alpha-1/latest")
    assert response.status_code == 200
    assert response.json()["satellite_id"] == "SAT-Alpha-1"