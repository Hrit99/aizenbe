
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    CORS(app)
    
    
    app.config.from_pyfile('config.py')

    
    db.init_app(app)
    jwt.init_app(app)

    
    with app.app_context():
        from .routes import auth_bp
        app.register_blueprint(auth_bp)

        
        db.create_all()

    return app
 
