from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO
from flask_mail import Mail

mail = Mail()
db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()
socketio = SocketIO(cors_allowed_origins="*")
