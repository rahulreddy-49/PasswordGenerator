from flask import Flask
from flask_cors import CORS
from config.config import Config
from models.models import db
from routes.api import api_bp
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable CORS for frontend requests
    CORS(app)
    
    # Initialize database
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')

    @app.route('/')
    def server_status():
        return {
            "status": "CipherVault API Online",
            "message": "To view the UI, please open the 'frontend/index.html' file in your browser.",
            "version": "2.0.0"
        }
    
    with app.app_context():
        db.create_all()
        
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
