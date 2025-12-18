from app.src.main import create_app

def test_health_returns_json():
    app = create_app()
    client = app.test_client()
    res = client.get("/health")
    assert res.is_json is True
