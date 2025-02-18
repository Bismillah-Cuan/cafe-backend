import os
from app.connections.db import Session
from flask import jsonify
from datetime import datetime
from collections import defaultdict
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from app.models.purchase_order_model import PurchaseOrder
from app.models.purchase_request_model import PurchaseRequest
from app.models.supplier_model import Supplier
from app.constant.messages.error import Error
from app.constant.messages.purchase_order import PurchaseOrderMessages
from app.constant.messages.supplier import SupplierMessages
from app.constant.enums.po_status import POStatus

class PurchaseOrderServices:
    @staticmethod
    def get_all_purchase_orders():
        with Session() as session:
            try:
                purchase_orders = session.query(PurchaseOrder).filter_by(is_deleted=False).all()
                
                #dictionary utk mengelompokkan PO berdasarkan po_code
                grouped_purchase_orders = defaultdict(lambda: {"po_code": "", "division": "", "user_id": "", "status": "", "requested_raw_materials": []})
                
                for po in purchase_orders:
                    po_data = po.to_dict()
                    
                    if po_data["po_code"] not in grouped_purchase_orders:
                        grouped_purchase_orders[po_data["po_code"]].update({
                            "po_code": po_data["po_code"],
                            "division": po_data["division"],
                            "user_id": po_data["user_id"],
                            "status": po_data["status"],
                            "requested_raw_materials": []
                        })
                        
                    if po.raw_materials:
                        raw_material_data = po.raw_materials.to_dict()
                        raw_material_data.pop("quantity", None)
                        raw_material_data.pop("metadata", None)
                        grouped_purchase_orders[po_data["po_code"]]["requested_raw_materials"].append({
                            "supplier_name": po.supplier.name if po.supplier else "",
                            "requested_quantity": po.purchase_request.quantity,
                            "requested_notes": po.purchase_request.notes,
                            "received_quantity": po.received_qty,
                            "received_notes": po.received_notes,
                            "supplier_notes": po.supplier_notes,
                            "raw_material_details": raw_material_data
                        })
                        
            except Exception as e:
                session.rollback()
                return jsonify(Error.messages(e)), 400
            
            return jsonify({
                "msg": PurchaseOrderMessages.SUCCESS_SHOW_ALL_PURCHASE_ORDER,
                "purchase_orders": list(grouped_purchase_orders.values())
            })
        
        #get nya klo ada received quantity yg ditunjukin received quantity

    @staticmethod
    def generate_pr_code(division):
        with Session() as session:
            try:
                if division == "super_admin":
                    div_prefix = "SA"
                elif division == "admin":
                    div_prefix = "AD"
                elif division == "kitchen":
                    div_prefix = "KT"
                elif division == "bar":
                    div_prefix = "BR"
                elif division == "sosmed":
                    div_prefix = "SM"
                elif division == "finance":
                    div_prefix = "FN"
                else:
                    return jsonify({"msg": "Invalid division"}), 400
                
                # Ambil kode terakhir yang ada
                last_po = (
                    session.query(PurchaseOrder)
                    .filter(PurchaseOrder.is_deleted == False)  # Menambahkan filter
                    .order_by(PurchaseOrder.id.desc())         # Mengurutkan berdasarkan id secara menurun
                    .first()                                     # Mengambil record pertama
                )

                last_po_code = last_po.po_code if last_po else None
                if last_po_code:
                    last_po_code = last_po_code.split("-")[2]
                    last_po_code = int(last_po_code) + 1
                else:    
                    last_po_code = 1

                # Buat pr_code baru
                new_pr_code = f"PO{div_prefix}-{datetime.now().strftime('%m%d')}-{last_po_code:04d}"

            except Exception as e:
                session.rollback()
                return jsonify(Error.messages(e)), 400

            return new_pr_code
        
    @staticmethod
    def create_purchase_order(data, payload):
        with Session() as session:
            try:
                # Ambil daftar pr_id dan rm_id berdasarkan pr_code
                pr_entries = session.query(PurchaseRequest.id, PurchaseRequest.raw_material_id).filter_by(pr_code=data["pr_code"]).all()

                # Pastikan ada entri yang ditemukan
                if pr_entries:
                    for pr_id, rm_id in pr_entries:
                        po = PurchaseOrder(
                            po_code=PurchaseOrderServices.generate_pr_code(pr_entries[0].division),  # Generate kode PO
                            purchase_request_id=pr_id,  # Gunakan pr_id dari hasil query
                            raw_material_id=rm_id,  # Gunakan rm_id dari hasil query
                            division=payload["division"],  # Ambil dari payload
                            user_id=payload["user_id"]  # Ambil dari payload
                        )
                        session.add(po)  # Tambahkan entri ke session
                    session.commit()  # Simpan perubahan ke database
            except Exception as e:
                session.rollback()
                return jsonify(Error.messages(e)), 400

            return jsonify({
                "msg": PurchaseOrderMessages.SUCCESS_CREATE_PURCHASE_ORDER
            }), 200
            
    @staticmethod
    def delete_purchase_order(data):
        with Session() as session:
            try:
                purchase_orders = session.query(PurchaseOrder).filter_by(po_code=data["po_code"]).all()
                if purchase_orders is None:
                    return jsonify({"msg": PurchaseOrderMessages.PURCHASE_ORDER_NOT_FOUND}), 404
                
                for po in purchase_orders:
                    po.is_deleted = True
                    po.po_code = f"deleted_{po.po_code}"
                    
                session.commit()
            except Exception as e:
                session.rollback()
                return jsonify(Error.messages(e)), 400
            
            return jsonify({
                "msg": PurchaseOrderMessages.SUCCESS_DELETE_PURCHASE_ORDER
            })
            
    @staticmethod
    def update_purchase_order(data):
        with Session() as session:
            try:
                if data["update_type"] == "status":
                    if data["status"] not in POStatus.get_all_po_status():
                        return jsonify({"msg": PurchaseOrderMessages.INVALID_PURCHASE_ORDER_STATUS}), 400
                    
                    po = session.query(PurchaseOrder).filter_by(po_code=data["po_code"]).all()
                    
                    if not po:
                        return jsonify({"msg": PurchaseOrderMessages.PURCHASE_ORDER_NOT_FOUND}), 404
                    
                    for po in po:
                        po.po_status = data["status"]
                    
                    session.commit()
                    
                    return jsonify({
                        "msg": PurchaseOrderMessages.SUCCESS_CHANGE_PURCHASE_ORDER_STATUS
                    }), 200
                    
                elif data["update_type"] == "supplier":
                    # Pastikan raw_request_name adalah daftar
                    if not isinstance(data.get("update_supplier"), list):
                        return jsonify({"msg": PurchaseOrderMessages.INVALID_UPDATE_SUPPLIER_FORMAT}), 400

                    for request in data["update_supplier"]:
                        raw_material_id = request.get("raw_material_id")
                        supplier_name = request.get("supplier_name")

                        if raw_material_id is None or not supplier_name:
                            return jsonify({"msg": PurchaseOrderMessages.INVALID_REQUEST_DATA}), 400

                        # Query supplier berdasarkan nama
                        supplier = session.query(Supplier).filter_by(name=supplier_name).first()
                        if supplier is None:
                            return jsonify({"msg": f"{SupplierMessages.SUPPLIER_NOT_FOUND} : {supplier_name}"}), 404

                        # Query PurchaseOrder berdasarkan po_code dan raw_material_id
                        po = session.query(PurchaseOrder).filter_by(po_code=data["po_code"], raw_material_id=raw_material_id).first()
                        if not po:
                            return jsonify({"msg": f"{PurchaseOrderMessages.PURCHASE_ORDER_NOT_FOUND_FOR_RAW_MATERIAL_ID} : {raw_material_id}"}), 404

                        # Update supplier_id pada PurchaseOrder
                        po.supplier_id = supplier.id

                    # Commit perubahan ke database
                    session.commit()

                    return jsonify({
                        "msg": PurchaseOrderMessages.SUCCESS_CHANGE_PURCHASE_ORDER_SUPPLIER
                    }), 200
                
                elif data["update_type"] == "supplier_notes":
                    supplier = session.query(Supplier).filter_by(name=data["supplier_name"]).first()
                    po = session.query(PurchaseOrder).filter_by(po_code=data["po_code"], supplier_id=supplier.id).all()
                    
                    if not po:
                        return jsonify({"msg": PurchaseOrderMessages.PURCHASE_ORDER_NOT_FOUND}), 404
                    
                    for po in po:
                        po.supplier_notes = data["supplier_notes"]
                    
                    session.commit()
                    
                    return jsonify({
                        "msg": PurchaseOrderMessages.SUCCESS_CHANGE_SUPPLIER_NOTES
                    }), 200
                    
                elif data["update_type"] == "received_data":
                    po = session.query(PurchaseOrder).filter_by(po_code=data["po_code"], raw_material_id=data["raw_material_id"]).first()
                    
                    if not po:
                        return jsonify({"msg": PurchaseOrderMessages.PURCHASE_ORDER_NOT_FOUND}), 404
                    
                    
                    po.received_qty = data["received_qty"]
                    po.received_notes = data["received_notes"]
                    
                    session.commit()
                    
                    return jsonify({
                        "msg": PurchaseOrderMessages.SUCCESS_CHANGE_RECEIVED_DATA
                    }), 200
                    
                else:
                    return jsonify({"msg": PurchaseOrderMessages.INVALID_UPDATE_TYPE}), 400
            except Exception as e:
                session.rollback()
                return jsonify(Error.messages(e)), 400
            
    @staticmethod
    def generate_receiving_form_html(data):
        with Session() as session:
            try:
                po = session.query(PurchaseOrder).filter_by(po_code=data["po_code"]).all()
                if not po:
                    return jsonify({"msg": PurchaseOrderMessages.PURCHASE_ORDER_NOT_FOUND}), 404

                data_pdf = {
                    "no_po": po[0].po_code,
                    "nama_supplier": po[0].supplier.name if po[0].supplier and po[0].supplier.name else "",
                    "rows": []
                }

                for po_item in po:
                    row = {
                        "material_name": po_item.raw_materials.name,
                        "requested_quantity": po_item.purchase_request.quantity,
                        "received_quantity": "",
                        "unit": po_item.raw_materials.purchase_unit,
                        "notes": "",
                        "condition": "Baik / Rusak"
                    }
                    data_pdf["rows"].append(row)

                # Path ke template HTML
                current_directory = os.getcwd()
                html_template_folder = os.path.abspath(os.path.join(current_directory, "app/constant/html_template"))

                # Load template HTML
                file_loader = FileSystemLoader(html_template_folder)
                env = Environment(loader=file_loader)
                template = env.get_template('receiving_form_template.html')

                # Render template dengan data tanpa menyimpannya ke file
                rendered_html = template.render(data_pdf)

                return jsonify({
                    "msg": PurchaseOrderMessages.SUCCESS_CREATE_RECEIVING_FORM,
                    "html": rendered_html
                }), 200

            except Exception as e:
                session.rollback()
                return jsonify(Error.messages(e)), 400
                
                
                    
                    
                    
                
                