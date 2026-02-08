from flask import Flask
from flask_cors import CORS
from .config import Config
from .extensions import db, jwt, bcrypt, socketio, mail
from .routes.auth import auth_bp
from flask_mail import Mail, Message
from app.routes.users import users_bp
from .routes.flights_proxy import flights_bp

def create_app():
    app = Flask(__name__)
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'   # ili tvoj SMTP server
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'lukaglishic@gmail.com'
    app.config['MAIL_PASSWORD'] = 'qebp doqo uqnr naim'  
    app.config['MAIL_DEFAULT_SENDER'] = 'lukaglishic@gmail.com'
    app.config.from_object(Config)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(flights_bp, url_prefix="/api")

    CORS(app)
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    socketio.init_app(app)
    mail.init_app(app)

    # with app.app_context():
    #     db.create_all()


    return app
