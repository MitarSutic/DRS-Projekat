from flask import Flask
from flask_cors import CORS
from .config import Config
from .extensions import db, jwt, bcrypt, socketio
from .routes.auth import auth_bp
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(auth_bp, url_prefix="/auth")

    CORS(app)
    db.init_app(app)
    migrate = Migrate()
    jwt.init_app(app)
    bcrypt.init_app(app)
    socketio.init_app(app)

    migrate.init_app(app,db)

    # with app.app_context():
    #     db.create_all()


    return app
