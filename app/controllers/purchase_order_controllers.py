from flask import request, jsonify
from app.services.purchase_order_services import PurchaseOrderServices
from app.utils.auth.protected_routes import division_required
from app.constant.messages.auth import AuthMessages

class PurchaseOrderControllers:
    @staticmethod
    @division_required("super_admin", "admin", "kitchen", "bar", "sosmed", "finance")
    def purchase_order_controllers(payload):
        division = payload["division"]
        if division == "super_admin" or division == "admin":
            if request.method == "GET":
                response = PurchaseOrderServices.get_all_purchase_orders()
            elif request.method == "POST":
                data = request.json
                response = PurchaseOrderServices.create_purchase_order(data, payload)
            elif request.method == "PUT":
                data = request.json
                response = PurchaseOrderServices.update_purchase_order(data)
            elif request.method == "DELETE":
                data = request.json
                response = PurchaseOrderServices.delete_purchase_order(data)
        else:
            if request.method == "GET":
                response = PurchaseOrderServices.get_all_purchase_orders()
            else:
                return jsonify(AuthMessages.USER_NOT_AUTHORIZED), 403

        return response