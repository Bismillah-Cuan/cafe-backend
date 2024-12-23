from flask import jsonify
from collections import defaultdict
from app.connections.db import Session
from app.models.purchase_request_model import PurchaseRequest
from app.models.raw_materials_model import RawMaterials
from app.models.users_model import Users
from app.constant.messages.purchase_request import PurchaseRequestMessages
from app.constant.messages.raw_materials import RawMaterialMessages
from app.constant.messages.user import UserMessages
from app.constant.messages.error import Error

class PurchaseRequestServices:
    @staticmethod
    def get_all_purchase_request():
        with Session() as session:
            try:
                # Ambil semua purchase request yang tidak dihapus
                purchase_requests = session.query(PurchaseRequest).filter(PurchaseRequest.is_deleted == False).all()
                
                # Dictionary untuk mengelompokkan PR berdasarkan pr_code
                grouped_purchase_requests = defaultdict(lambda: {"pr_code": "", "division": "", "user_id": "", "status": "", "metadata": {}, "requested_raw_materials": []})

                # Iterasi semua purchase_request
                for purchase_request in purchase_requests:
                    # Ambil data PR dalam bentuk dictionary
                    pr_data = purchase_request.to_dict()

                    # Jika belum ada dalam dictionary, inisialisasi key baru
                    if pr_data["pr_code"] not in grouped_purchase_requests:
                        grouped_purchase_requests[pr_data["pr_code"]].update({
                            "pr_code": pr_data["pr_code"],
                            "division": pr_data["division"],
                            "user_id": pr_data["user_id"],
                            "status": pr_data["status"],
                            "metadata": pr_data.get("metadata", {}),
                            "requested_raw_materials": []  # Kosongkan requested_raw_materials awalnya
                        })

                    # Jika raw_material ada, tambahkan ke requested_raw_materials
                    if purchase_request.raw_materials:
                        raw_material_data = purchase_request.raw_materials.to_dict()  # Ambil dict raw_material
                        raw_material_data.pop("quantity", None)  # Hapus quantity jika ada
                        raw_material_data.pop("metadata", None)  # Hapus metadata jika ada

                        # Tambahkan raw_material ke list
                        grouped_purchase_requests[pr_data["pr_code"]]["requested_raw_materials"].append({
                            "raw_material_id": purchase_request.raw_materials.id,
                            "quantity": purchase_request.quantity,  # Ambil quantity dari PurchaseRequest
                            "details": raw_material_data  # Details berisi raw_material fields kecuali quantity
                        })

                # Konversi defaultdict ke list biasa
                response_data = list(grouped_purchase_requests.values())

                # Berikan respons JSON
                return jsonify({
                    "message": PurchaseRequestMessages.SUCCESS_SHOW_PURCHASE_REQUEST,
                    "pr_list": response_data
                }), 200
            
            except Exception as e:
                return jsonify({"error": str(e)}), 400

            
    @staticmethod
    def get_purchase_request(data):
        with Session() as session:
            try:
                # Ambil semua purchase request dengan pr_code yang diberikan
                purchase_requests = session.query(PurchaseRequest).filter_by(pr_code=data["pr_code"]).all()
                
                # Validasi apakah data ditemukan
                if not purchase_requests:  # Cek apakah daftar kosong
                    return jsonify({"msg": PurchaseRequestMessages.PURCHASE_REQUEST_NOT_FOUND}), 400
                
                # Konversi setiap objek ke dictionary dan exclude quantity dari raw materials
                list_purchase_requests = []
                for pr in purchase_requests:
                    pr_data = pr.to_dict()
                    # Ambil raw_materials yang sesuai, tanpa quantity
                    requested_raw_materials = []
                    for raw_material in pr.raw_materials:
                        rm_data = raw_material.to_dict()
                        rm_data.pop('quantity', None)  # Hapus quantity dari raw_material
                        requested_raw_materials.append({
                            "raw_material_id": rm_data.id,
                            "quantity": pr.quantity,  # Gunakan quantity dari PurchaseRequest
                            "details": rm_data  # Details tetap berisi data selain quantity
                        })
                    
                    pr_data["requested_raw_materials"] = requested_raw_materials
                    list_purchase_requests.append(pr_data)
                
                return jsonify({
                    "message": PurchaseRequestMessages.SUCCESS_SHOW_PURCHASE_REQUEST,
                    "purchase_requests": list_purchase_requests
                }), 200
            except Exception as e:
                return jsonify(Error.messages(e)), 400


            
    @staticmethod
    def create_purchase_request(data, payload):
        with Session() as session:
            try:
                # Pisahkan raw_material_id dan quantity menjadi daftar
                raw_material_ids = list(map(str.strip, str(data["raw_material_id"]).split(',')))
                quantities = list(map(str.strip, str(data["quantity"]).split(',')))

                # Pastikan jumlah raw_material_ids sama dengan quantities
                if len(raw_material_ids) != len(quantities):
                    return jsonify({"msg": PurchaseRequestMessages.RAW_MATERIAL_QUANTITY_MISMATCH}), 400

                # Iterasi setiap pasangan raw_material_id dan quantity
                purchase_requests = []
                for raw_material_id, quantity in zip(raw_material_ids, quantities):
                    # Cek jika ada purchase request dengan kombinasi pr_code dan raw_material_id yang sama
                    existing_purchase_request = session.query(PurchaseRequest).filter_by(
                        pr_code=data["pr_code"], raw_material_id=raw_material_id
                    ).first()

                    if existing_purchase_request:
                        # Ambil nama material atau detail lainnya untuk dimasukkan dalam respons
                        raw_material = session.query(RawMaterials).filter_by(id=raw_material_id).first()
                        if raw_material:
                            raw_material_name = raw_material.name
                        else:
                            return jsonify({"msg": RawMaterialMessages.RAW_MATERIALS_NOT_FOUND}), 404
                        
                        return jsonify(
                            {
                                "msg": PurchaseRequestMessages.RAW_MATERIAL_ALREADY_ADDED,
                                "material": {
                                    "id": raw_material_id,
                                    "name": raw_material_name,
                                },
                            }
                        ), 400
                        
                    # Jika tidak ditemukan, cek validitas raw_material_id
                    raw_material = session.query(RawMaterials).filter_by(id=raw_material_id).first()
                    if raw_material is None:
                        return jsonify({"msg": RawMaterialMessages.RAW_MATERIALS_NOT_FOUND}), 404

                    # Buat instance PurchaseRequest
                    purchase_request = PurchaseRequest(
                        pr_code=data["pr_code"],
                        user_id=payload["user_id"],
                        division=payload["division"],
                        raw_material_id=raw_material_id,
                        quantity=quantity
                    )
                    session.add(purchase_request)
                    purchase_requests.append(purchase_request)

                # Commit setelah semua entri ditambahkan
                session.commit()

                # Convert semua purchase request ke dict untuk respon
                purchase_requests_dict = [pr.to_dict() for pr in purchase_requests]

            except Exception as e:
                session.rollback()
                return jsonify(Error.messages(e)), 400

            # Respon sukses
            return jsonify({
                "message": PurchaseRequestMessages.SUCCESS_CREATE_PURCHASE_REQUEST,
                "purchase_requests": purchase_requests_dict
            }), 200

            
    @staticmethod
    def delete_purchase_request(data):
        with Session() as session:
            try:
                # Cari semua entri dengan pr_code
                purchase_requests = session.query(PurchaseRequest).filter_by(pr_code=data["pr_code"]).all()
                
                # Validasi apakah data ada
                if not purchase_requests:  # Cek apakah daftar kosong
                    return jsonify({"msg": PurchaseRequestMessages.PURCHASE_REQUEST_NOT_FOUND}), 400
                
                # Tandai semua entri dengan is_deleted = True
                for pr in purchase_requests:
                    pr.is_deleted = True
                
                # Simpan perubahan
                session.commit()

            except Exception as e:
                session.rollback()
                return jsonify(Error.messages(e)), 400

            return jsonify({
                "message": PurchaseRequestMessages.SUCCESS_DELETE_PURCHASE_REQUEST
            }), 200

            
    @staticmethod
    def update_purchase_request(data):
        with Session() as session:
            try:
                # Ambil semua PurchaseRequest dengan pr_code tertentu
                purchase_requests = session.query(PurchaseRequest).filter_by(pr_code=data["pr_code"]).all()
                if not purchase_requests:
                    return jsonify({"msg": PurchaseRequestMessages.PURCHASE_REQUEST_NOT_FOUND}), 400

                # Pisahkan raw_material_id dan quantity menjadi daftar
                raw_material_ids = list(map(str.strip, str(data["raw_material_id"]).split(',')))
                quantities = list(map(str.strip, str(data["quantity"]).split(',')))

                # Validasi panjang raw_material_id dan quantity
                if len(raw_material_ids) != len(quantities):
                    return jsonify({"msg": PurchaseRequestMessages.RAW_MATERIAL_QUANTITY_MISMATCH}), 400

                # Hapus entri lama yang tidak ada di raw_material_id baru
                for pr in purchase_requests:
                    if str(pr.raw_material_id) not in raw_material_ids:
                        session.delete(pr)

                # Update atau tambahkan entri baru
                for raw_material_id, quantity in zip(raw_material_ids, quantities):
                    pr = session.query(PurchaseRequest).filter_by(
                        pr_code=data["pr_code"], raw_material_id=raw_material_id
                    ).first()
                    if pr:
                        # Jika entri ada, perbarui field-nya
                        pr.user_id = data["user_id"]
                        pr.division = data["division"]
                        pr.quantity = quantity
                    else:
                        # Jika tidak ada, buat entri baru
                        new_pr = PurchaseRequest(
                            pr_code=data["pr_code"],
                            raw_material_id=raw_material_id,
                            user_id=data["user_id"],
                            division=data["division"],
                            quantity=quantity
                        )
                        session.add(new_pr)

                # Commit semua perubahan
                session.commit()

                # Ambil semua PurchaseRequest terbaru untuk pr_code
                updated_purchase_requests = session.query(PurchaseRequest).filter_by(pr_code=data["pr_code"]).all()

                # Format response untuk setiap purchase_request
                updated_requests_dict = []
                for pr in updated_purchase_requests:
                    pr_data = pr.to_dict()

                    # Ambil raw_materials yang sesuai, tanpa quantity
                    requested_raw_materials = []
                    for raw_material in pr.raw_materials:
                        rm_data = raw_material.to_dict()
                        rm_data.pop('quantity', None)  # Hapus quantity dari raw_material
                        requested_raw_materials.append({
                            "raw_material_id": rm_data.id,
                            "quantity": pr.quantity,  # Gunakan quantity dari PurchaseRequest
                            "details": rm_data  # Details tetap berisi data selain quantity
                        })
                    
                    pr_data["requested_raw_materials"] = requested_raw_materials
                    updated_requests_dict.append(pr_data)

            except Exception as e:
                session.rollback()
                return jsonify(Error.messages(e)), 400

            # Respon sukses
            return jsonify({
                "message": PurchaseRequestMessages.SUCCESS_UPDATE_PURCHASE_REQUEST,
                "updated_purchase_requests": updated_requests_dict
            }), 200


