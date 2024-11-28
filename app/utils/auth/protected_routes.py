from flask import jsonify
import json
from functools import wraps
from app.constant.messages.auth import AuthMessages
from app.constant.messages.user import  UserMessages
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models.users_model import Users
from app.connections.db import Session

# Custom decorator to check division
def division_required(*division):
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorated_view(*args, **kwargs):
            payload = eval(get_jwt_identity())
            with Session() as session:
                if payload["division"] not in division:
                    return jsonify({"msg": AuthMessages.USER_NOT_AUTHORIZED}), 403
                
                user = session.query(Users).filter_by(username = payload["username"])
                if user is None:
                    return jsonify({"msg": UserMessages.USERNAME_NOT_EXIST}), 404
            return fn(payload, *args, **kwargs)
        return decorated_view
    return wrapper