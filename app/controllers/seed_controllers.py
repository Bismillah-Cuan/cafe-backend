from flask import request
from app.services.seed_services import SeedsService

def seeds_controller():
    if request.method == "GET":
        response = SeedsService.show_seeds()
        
        return response
    
    if request.method == "POST":
        response = SeedsService.generate_all_seed()
        
        return response
    
    if request.method == "DELETE":
        response = SeedsService.clear_seeds()
        
        return response