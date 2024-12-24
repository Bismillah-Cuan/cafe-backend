from flask import jsonify
from app.connections.db import Session
from app.models.supplier_model import Supplier
from app.constant.messages.supplier import SupplierMessages
from app.constant.messages.error import Error

class SupplierServices:
    @staticmethod
    def get_all_suppliers():
        with Session() as session:
            try:
                suppliers: Supplier = session.query(Supplier).filter(Supplier.is_deleted == False).all()
                
                list_suppliers = [supplier.to_dict() for supplier in suppliers]
                
                return jsonify({
                    "message": SupplierMessages.SUCCESS_SHOW_ALL_SUPPLIER,
                    "suppliers": list_suppliers
                })
            except Exception as e:
                return jsonify(Error.messages(e))
    
    @staticmethod
    def create_supplier(data):
        with Session() as session:
            try:
                check_name = session.query(Supplier).filter_by(name=data["name"]).first()
                if check_name is not None:
                    return jsonify({"msg": SupplierMessages.SUPPLIER_ALREADY_EXIST}), 400
                
                address = data["address"].strip() if data.get("address", "").strip() else None
                phone_number = data["phone_number"].strip() if data.get("phone_number", "").strip() else None
                
                new_supplier: Supplier = Supplier(
                    name = data["name"],
                    address = address,
                    phone_number = phone_number
                )
                session.add(new_supplier)
                session.commit()
            except Exception as e:
                session.rollback()
                return jsonify(Error.messages(e)), 400
            
            return jsonify({
                "msg": SupplierMessages.SUCCESS_ADD_SUPPLIER_DATA,
                "new_supplier": new_supplier.to_dict()
            }), 201
            
    @staticmethod
    def delete_supplier(data):
        with Session() as session:
            try:
                check_supplier = session.query(Supplier).filter_by(id=data["id"], name=data["name"]).first()
                if check_supplier is None:
                    return jsonify({"msg": SupplierMessages.SUPPLIER_NOT_FOUND}), 404
                
                check_supplier.is_deleted = True
                session.commit()
            except Exception as e:
                session.rollback()
                return jsonify(Error.messages(e)), 400
            
            return jsonify({
                "msg": SupplierMessages.SUCCESS_DELETE_SUPPLIER_DATA
            }), 200
            
    @staticmethod
    def update_supplier(data):
        with Session() as session:
            try:
                check_supplier = session.query(Supplier).filter_by(id=data["id"], name=data["name"]).first()
                if check_supplier is None:
                    return jsonify({"msg": SupplierMessages.SUPPLIER_NOT_FOUND}), 404
                check_supplier.name = data["name"]
                
                check_supplier.address = data["address"].strip() if data.get("address", "").strip() else None
                check_supplier.phone_number = data["phone_number"].strip() if data.get("phone_number", "").strip() else None
                
                session.add(check_supplier)
                session.commit()
            except Exception as e:
                session.rollback()
                return jsonify(Error.messages(e)), 400
            
            return jsonify({
                "msg": SupplierMessages.SUCCESS_UPDATE_SUPPLIER_DATA,
                "updated_supplier": check_supplier.to_dict()
            }), 200