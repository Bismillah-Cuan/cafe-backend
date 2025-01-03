from flask import jsonify
from app.connections.db import Session
from app.models.raw_materials_model import RawMaterials
from app.constant.messages.raw_materials import RawMaterialMessages
from app.constant.messages.error import Error

class RawMaterialServices:
    @staticmethod
    def get_all_raw_materials():
        with Session() as session:
            try:
                raw_materials = session.query(RawMaterials).filter(RawMaterials.is_deleted == False).all()
                list_raw_materials = [raw_material.to_dict() for raw_material in raw_materials]
                
                return jsonify({
                    "messages": RawMaterialMessages.SUCCESS_SHOW_ALL_RAW_MATERIALS,
                    "raw_materials": list_raw_materials
                })
            except Exception as e:
                return jsonify(Error.messages(e))
            
    @staticmethod
    def get_raw_materials_by_word(word):
        with Session() as session:
            try:
                raw_materials = session.query(RawMaterials).filter(RawMaterials.name.contains(word), RawMaterials.is_deleted == False).all()
                list_raw_materials = [raw_material.to_dict() for raw_material in raw_materials]
                
                return jsonify({
                    "messages": RawMaterialMessages.SUCCESS_SHOW_ALL_RAW_MATERIALS,
                    "raw_materials": list_raw_materials
                })
            except Exception as e:
                return jsonify(Error.messages(e))
            
    @staticmethod
    def create_raw_material(data):
        with Session() as session:
            try:
                check_raw_material = session.query(RawMaterials).filter(
                    RawMaterials.name == data["name"], 
                    RawMaterials.is_deleted == False
                ).first()

                if check_raw_material is not None:
                    return jsonify({"msg": RawMaterialMessages.RAW_MATERIALS_ALREADY_EXIST}), 400
                
                new_raw_material: RawMaterials = RawMaterials(
                    name = data["name"],
                    type = data["type"],
                    brand = data["brand"],
                    purchase_unit = data["purchase_unit"],
                    quantity = data["quantity"],
                    quantity_unit = data["quantity_unit"]
                )
                
                session.add(new_raw_material)
                session.commit()
            except Exception as e:
                session.rollback()
                return jsonify(Error.messages(e)), 400
            
            return jsonify({
                "msg": RawMaterialMessages.SUCCESS_ADD_RAW_MATERIALS_DATA,
                "new_raw_material": new_raw_material.to_dict()
            })
            
    @staticmethod
    def update_raw_material(data):
        with Session() as session:
            try:
                check_raw_material = session.query(RawMaterials).filter_by(id=data["id"], name=data["name"]).first()
                if check_raw_material is None:
                    return jsonify({"msg": RawMaterialMessages.RAW_MATERIALS_NOT_FOUND}), 404
                
                check_raw_material.name = data["name"]
                check_raw_material.type = data["type"]
                check_raw_material.brand = data["brand"]
                check_raw_material.purchase_unit = data["purchase_unit"]
                check_raw_material.quantity = data["quantity"]
                check_raw_material.quantity_unit = data["quantity_unit"]
                
                session.add(check_raw_material)
                session.commit()
            except Exception as e:
                session.rollback()
                return jsonify(Error.messages(e)), 400
            
            return jsonify({
                "msg": RawMaterialMessages.SUCCESS_UPDATE_RAW_MATERIALS_DATA,
                "updated_raw_material": check_raw_material.to_dict()
            })
            
    @staticmethod
    def delete_raw_material(data):
        with Session() as session:
            try:
                check_raw_material = session.query(RawMaterials).filter_by(id=data["id"], name=data["name"]).first()
                if check_raw_material is None:
                    return jsonify({"msg": RawMaterialMessages.RAW_MATERIALS_NOT_FOUND}), 404
                
                check_raw_material.is_deleted = True
                session.commit()
            except Exception as e:
                session.rollback()
                return jsonify(Error.messages(e)), 400
            
            return jsonify({
                "msg": RawMaterialMessages.SUCCESS_DELETE_RAW_MATERIALS_DATA
            })