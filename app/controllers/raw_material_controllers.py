from flask import request, jsonify
from app.services.raw_material_services import RawMaterialServices
from app.utils.auth.protected_routes import division_required
from app.constant.messages.error import Error

class RawMaterialControllers:
    @staticmethod
    @division_required("super_admin", "admin", "kitchen", "bar", "sosmed", "finance")
    def raw_materials_controllers(payload):
        division = payload["division"]
        
        if division == "super_admin":
            if request.method == "GET":
                response = RawMaterialServices.get_all_raw_materials()
            elif request.method == "POST":
                data = request.json
                response = RawMaterialServices.create_raw_material(data)
            elif request.method == "PUT":
                data = request.json
                response = RawMaterialServices.update_raw_material(data)
            elif request.method == "DELETE":
                data = request.json
                response = RawMaterialServices.delete_raw_material(data)
        else:
            if request.method == "GET":
                response = RawMaterialServices.get_all_raw_materials()
        
        return response