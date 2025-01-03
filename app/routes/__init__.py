from flask import Blueprint
from flask_cors import CORS
from app.controllers.users_controllers import UsersController
from app.controllers.raw_material_controllers import RawMaterialControllers
from app.controllers.supplier_controllers import SupplierControllers
from app.controllers.purchase_request_controllers import PurchaseRequestControllers
from app.controllers.seed_controllers import seeds_controller

users = Blueprint("users", __name__)
users.add_url_rule("/register", view_func=UsersController.register_user, methods=["POST"])
users.add_url_rule("/login", view_func=UsersController.login_user, methods=["POST"])
users.add_url_rule("/delete", view_func=UsersController.delete_user, methods=["DELETE"])
users.add_url_rule("/profiles", view_func=UsersController.user_profile, methods=["GET"])
users.add_url_rule("/profiles/change-password", view_func=UsersController.change_password, methods=["PUT"])
users.add_url_rule("/create-admin", view_func=UsersController.create_user, methods=["POST"])

raw_materials = Blueprint("raw-materials", __name__)
raw_materials.add_url_rule("/", view_func=RawMaterialControllers.raw_materials_controllers, methods=["GET", "POST", "DELETE", "PUT"])
raw_materials.add_url_rule("/search", view_func=RawMaterialControllers.search_raw_material, methods=["POST"])

suppliers = Blueprint("suppliers", __name__)
suppliers.add_url_rule("/", view_func=SupplierControllers.supplier_controllers, methods=["GET", "POST", "DELETE", "PUT"])

purchase_request = Blueprint("purchase-request", __name__)
purchase_request.add_url_rule("/", view_func=PurchaseRequestControllers.purchase_request_controllers, methods=["GET", "POST", "DELETE", "PUT"])
purchase_request.add_url_rule("/change-status", view_func=PurchaseRequestControllers.change_status, methods=["PUT"])

seeds = Blueprint("seeds", __name__)
seeds.add_url_rule("/", view_func=seeds_controller, methods=["GET", "POST", "DELETE"])