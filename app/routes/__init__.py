from flask import Blueprint
from app.controllers.users_controllers import UsersController
from app.controllers.seed_controllers import seeds_controller

users = Blueprint("users", __name__)
users.add_url_rule("/register", view_func=UsersController.create_user, methods=["POST"])
users.add_url_rule("/login", view_func=UsersController.login_user, methods=["POST"])
users.add_url_rule("/me", view_func=UsersController.user_profile, methods=["GET"])
users.add_url_rule("/me/change-password", view_func=UsersController.change_password, methods=["PUT"])

seeds = Blueprint("seeds", __name__)
seeds.add_url_rule("/", view_func=seeds_controller, methods=["GET", "POST", "DELETE"])