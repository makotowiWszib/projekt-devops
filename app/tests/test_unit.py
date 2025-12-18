from app.src.config import Settings

def test_db_uri_exists():
    assert "postgresql" in Settings.SQLALCHEMY_DATABASE_URI
