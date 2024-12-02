from flask import jsonify
from app.connections.db import Session
from app.models.users_model import Users
from app.constant.messages.user import UserMessages
from app.constant.messages.error import Error

class UsersService:
    @staticmethod
    def create_user(data):
        with Session() as session:
            try:
                check_username = session.query(Users).filter_by(username=data["username"]).first()
                if check_username is not None:
                    return jsonify({"msg": UserMessages.USERNAME_ALREADY_EXIST}), 400
                new_user: Users = Users(
                    username = data["username"],
                    division = data["division"]
                )
                new_user.set_password(data["password"])
                
                session.add(new_user)
                session.commit()
            except Exception as e:
                session.rollback()
                return jsonify(Error.messages(e)), 400
            
            return jsonify({
                "msg": UserMessages.SUCCESS_USER_REGISTER,
                "new_user_info": new_user.to_dict()
            }), 201
    
    @staticmethod
    def login_user(data):
        username = data["username"]
        password = data["password"]
        
        with Session() as session:
            try:
                user_check: Users = session.query(Users).filter(Users.username == username).first()
                if user_check is None:
                    return jsonify({"msg": UserMessages.USERNAME_NOT_EXIST}), 404
                
                if user_check.check_password(password):
                    payload = {
                        "user_id": user_check.id,
                        "username": user_check.username,
                        "division": user_check.division.value
                    }
                    
                    return {
                        "msg": UserMessages.LOGIN_SUCCESS,
                        "payload": payload
                    }
                
                else:
                    return jsonify({"msg": UserMessages.INCORRECT_PASSWORD}), 403
            except Exception as e:
                return jsonify(Error.messages(e)), 400
            
    @staticmethod
    def user_profile(payload):
        with Session() as session:
            try:
                user_profile = session.query(Users).filter_by(id=payload["user_id"], username=payload["username"]).first()
                return jsonify({
                    "profile": user_profile.to_dict()
                }), 200
            except Exception as e:
                session.rollback()
                return jsonify(Error.messages(e)), 400
            
    def user_list():
        with Session() as session:
            try:
                users = session.query(Users).filter(Users.is_deleted == False).all()
                return jsonify({
                    "users": [user.to_dict() for user in users]
                }), 200
            except Exception as e:
                session.rollback()
                return jsonify(Error.messages(e)), 400
            
    @staticmethod
    def change_password(payload, data):
        with Session() as session:
            try:
                user_profile = session.query(Users).filter_by(id=payload["user_id"], username=payload["username"]).first()
                
                if not user_profile:
                    return jsonify({"msg": UserMessages.USERNAME_NOT_EXIST}), 404
            
                if not user_profile.check_password(data["old_password"]):
                    return jsonify({"msg": UserMessages.INCORRECT_PASSWORD}), 403

                user_profile.set_password(data["new_password"])
                session.commit()
                
                return jsonify({
                    "msg": UserMessages.SUCCESS_CHANGE_PASSWORD
                }), 200
            except Exception as e:
                session.rollback()
                return jsonify({
                    "msg": Error.messages(e)
                })
                
    @staticmethod
    def delete_user(data):
        with Session() as session:
            try:
                user_profile = session.query(Users).filter_by(id=data["id"], username=data["username"]).first()
                if not user_profile:
                    return jsonify({"msg": UserMessages.USERNAME_NOT_EXIST}), 404
                
                user_profile.is_deleted = True
                session.commit()
            except Exception as e:
                session.rollback()
                return jsonify(Error.messages(e)), 400
            
            return jsonify({
                "msg": UserMessages.SUCCESS_DELETE_USER
            }), 200
            