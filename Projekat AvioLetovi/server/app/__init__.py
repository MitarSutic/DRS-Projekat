from flask import Flask
from flask_cors import CORS
from .config import Config
from .extensions import db, jwt, bcrypt, socketio
from .routes.auth import auth_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(auth_bp, url_prefix="/auth")

    CORS(app)
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    socketio.init_app(app)

    return app
