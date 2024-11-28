from flask import jsonify
from app.connections.db import Session
from app.models.users_model import Users
from app.seeds.user_seeds import users_data
from app.constant.messages.seeds import SeedMessages
from app.constant.messages.error import Error
from sqlalchemy import text
from app.constant.SQL import Query

class SeedsService:
    @staticmethod
    def generate_all_seed():
        new_users = []
        with Session() as session:
            try:
                # Check User Data
                check_users = session.query(Users).count()
                
                if (check_users != 0):
                    return jsonify({
                        "msg": SeedMessages.SEEDS_ALREADY_EXIST
                    }), 400
                    
                # Generate User data
                for user in users_data:
                    new_user: Users = Users(
                        username=user["username"],
                        division=user["division"]
                    )
                    
                    new_user.set_password(user["password"])
                    
                    new_users.append(new_user)
                    
                session.add_all(new_users)
                session.commit()
                
                return jsonify({
                    "msg": SeedMessages.SUCCESS_ADD_SEEDS_DATA
                }), 201
            except Exception as e:
                session.rollback()
                return jsonify(Error.messages(e)), 400
    
    @staticmethod
    def show_seeds():
        with Session() as session:
            try:
                users =  session.query(Users).all()
                list_users = [user.to_dict() for user in users]
                
                return jsonify({
                    "msg": SeedMessages.SUCCESS_SHOW_ALL_SEED,
                    "users": list_users
                })
            except Exception as e:
                session.rollback()
                return jsonify(Error.messages(e))
    
    @staticmethod
    def clear_seeds():
        with Session() as session:
            try:
                session.query(Users).delete()
                session.execute(text(Query.reset_primary_key("users")))
                
                session.commit()
                
                return jsonify({
                    "msg": SeedMessages.CLEAR_SEEDS_DATA
                }), 200
            except Exception as e:
                session.rollback()
                return jsonify(Error.messages(e)), 400