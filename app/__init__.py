from flask import Flask
from app.routes.upload import upload_bp
import os

def create_app():
    app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), '../templates'))

    app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(__file__), '../uploads')

    app.register_blueprint(upload_bp)

    return app
