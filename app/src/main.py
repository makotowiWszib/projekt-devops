from flask import Flask, jsonify, request
from .config import Settings
from .db import db, migrate
from .models import User

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Settings)

    db.init_app(app)
    migrate.init_app(app, db)

    @app.get("/health")
    def health():
        return jsonify(status="ok"), 200

    @app.get("/users")
    def list_users():
        users = User.query.order_by(User.id.asc()).all()
        return jsonify([{"id": u.id, "email": u.email, "created_at": u.created_at.isoformat()} for u in users]), 200

    @app.post("/users")
    def create_user():
        payload = request.get_json(force=True)
        email = (payload.get("email") or "").strip()
        if not email:
            return jsonify(error="email is required"), 400
        u = User(email=email)
        db.session.add(u)
        db.session.commit()
        return jsonify(id=u.id, email=u.email), 201

    @app.get("/db-check")
    def db_check():
        db.session.execute(db.text("SELECT 1"))
        return jsonify(db="ok"), 200

    return app

app = create_app()
