from flask import Flask, redirect
from app.config import DevelopmentConfig, ProductionConfig
from flask_jwt_extended import JWTManager
from app.models.users_model import Users
from app.connections.db import Base, engine
import os

jwt = JWTManager()

def create_app(test_config=None, production_config=os.getenv("PRODUCTION_CONFIG")):
    app = Flask(__name__)
    
    Base.metadata.create_all(engine)
    
    if test_config is not None:
        app.config.from_object(test_config)
        
    if production_config is not None:
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)
        
    jwt.init_app(app)
    
    @app.route("/")
    def index():
        return redirect("https://documenter.getpostman.com/view/31842216/2sAYBRGa1z")
    
    from app.routes import users, raw_materials, seeds
    app.register_blueprint(users, url_prefix="/api/v1/users")
    app.register_blueprint(raw_materials, url_prefix="/api/v1/raw-materials")
    app.register_blueprint(seeds, url_prefix="/api/v1/seeds")
    
    return app