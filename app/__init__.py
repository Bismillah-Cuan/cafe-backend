from flask import Flask, redirect, request
from app.config import DevelopmentConfig, ProductionConfig
from flask_jwt_extended import JWTManager
import os
from flask_cors import CORS

jwt = JWTManager()

def create_app(test_config=None, production_config=os.getenv("PRODUCTION_CONFIG")):
    app = Flask(__name__)
    
    if test_config is not None:
        app.config.from_object(test_config)
        
    if production_config is not None:
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)
        
    jwt.init_app(app)
    
    CORS(app)
    
    @app.route("/")
    def index():
        return redirect("https://documenter.getpostman.com/view/31842216/2sAYBRGa1z")
    
    from app.routes import users, raw_materials, suppliers, seeds
    app.register_blueprint(users, url_prefix="/api/v1/users")
    app.register_blueprint(raw_materials, url_prefix="/api/v1/raw-materials")
    app.register_blueprint(suppliers, url_prefix="/api/v1/suppliers")
    app.register_blueprint(seeds, url_prefix="/api/v1/seeds")
    
    return app