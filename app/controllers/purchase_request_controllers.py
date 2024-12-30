from flask import request, jsonify
from app.services.purchase_request_services import PurchaseRequestServices
from app.utils.auth.protected_routes import division_required
from app.constant.messages.auth import AuthMessages

class PurchaseRequestControllers:
    @staticmethod
    @division_required("super_admin", "admin", "kitchen", "bar", "sosmed", "finance")
    def purchase_request_controllers(payload):
        division = payload["division"]
        
        if division == "super_admin" or division == "admin":
            if request.method == "GET":
                response = PurchaseRequestServices.get_all_purchase_request()
            elif request.method == "POST":
                data = request.json
                response = PurchaseRequestServices.create_purchase_request(data, payload)
            elif request.method == "PUT":
                data = request.json
                response = PurchaseRequestServices.update_purchase_request(data, payload)
            elif request.method == "DELETE":
                data = request.json
                response = PurchaseRequestServices.delete_purchase_request(data)
        else:
            if request.method == "GET":
                response = PurchaseRequestServices.get_all_purchase_request()
            elif request.method == "POST":
                data = request.json
                response = PurchaseRequestServices.create_purchase_request(data, payload)
            else:
                return jsonify(AuthMessages.USER_NOT_AUTHORIZED), 403
            
        return response
    
    @staticmethod
    @division_required("super_admin", "admin")
    def change_status(payload):
        _ = payload
        data = request.json
        
        response = PurchaseRequestServices.change_status(data)
        
        return response
    
    @staticmethod
    @division_required("super_admin", "admin", "kitchen", "bar", "sosmed", "finance")
    def generate_pr_code(payload):
        
        response = PurchaseRequestServices.generate_pr_code(payload)
        
        return response
            
            