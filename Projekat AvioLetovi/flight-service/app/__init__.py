from flask import Flask
from .extensions import db, jwt
from .routes.flights import flights_bp
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(flights_bp, url_prefix="/api/flights")

    with app.app_context():
        db.create_all()
    return app