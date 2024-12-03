from flask import Blueprint
from app.controllers.users_controllers import UsersController
from app.controllers.raw_material_controllers import RawMaterialControllers
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

seeds = Blueprint("seeds", __name__)
seeds.add_url_rule("/", view_func=seeds_controller, methods=["GET", "POST", "DELETE"])