from app import create_app
from app.extensions import socketio
from app.routes.admin import admin_bp

app = create_app()

app.register_blueprint(admin_bp, url_prefix="/admin")
if __name__ == "__main__":


    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
