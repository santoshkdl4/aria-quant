from app.core.config import settings

def test_config():
    assert settings.ENVIRONMENT in ["development", "production", "test"]
    assert settings.LIVE_TRADING_ENABLED is False
