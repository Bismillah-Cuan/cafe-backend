from flask import request, jsonify
from app.services.supplier_services import SupplierServices
from app.utils.auth.protected_routes import division_required
from app.constant.messages.auth import AuthMessages

class SupplierControllers:
    @staticmethod
    @division_required("super_admin", "admin")
    def supplier_controllers(payload):
        division = payload["division"]
        
        if division == "super_admin" or division == "admin":
            if request.method == "GET":
                response = SupplierServices.get_all_suppliers()
            elif request.method == "POST":
                data = request.json    
                response = SupplierServices.create_supplier(data)
            elif request.method == "PUT":            
                data = request.json
                response = SupplierServices.update_supplier(data)
            elif request.method == "DELETE":
                data = request.json
                response = SupplierServices.delete_supplier(data)
        else:
            if request.method == "GET":
                response = SupplierServices.get_all_suppliers()
            else:
                return jsonify(AuthMessages.USER_NOT_AUTHORIZED), 403
        
        return response