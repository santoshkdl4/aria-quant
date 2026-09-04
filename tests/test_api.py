from fastapi.testclient import TestClient
from app.main import app

def test_system_health():
    with TestClient(app) as client:
        response = client.get("/api/system/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "cpu_percent" in data
        assert "memory_percent" in data
        assert "disk_free_gb" in data
