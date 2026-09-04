from fastapi.testclient import TestClient
from app.main import app

def test_trading_engine():
    with TestClient(app) as client:
        # Fetch Initial Portfolio
        resp_init = client.get("/api/trading/portfolio")
        initial_data = resp_init.json()["data"]
        initial_qty = 0
        if "RELIANCE" in initial_data["positions"]:
            initial_qty = initial_data["positions"]["RELIANCE"]["qty"]
            
        # Buy
        resp = client.post("/api/trading/execute_mock", json={
            "symbol": "RELIANCE",
            "side": "BUY",
            "qty": 10,
            "price": 2500.0
        })
        assert resp.status_code == 200
        assert resp.json()["status"] == "success"
        
        # Check Portfolio
        resp2 = client.get("/api/trading/portfolio")
        assert resp2.status_code == 200
        data = resp2.json()["data"]
        assert "RELIANCE" in data["positions"]
        assert data["positions"]["RELIANCE"]["qty"] == initial_qty + 10
