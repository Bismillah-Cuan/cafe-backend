from app.models.users_model import Users
from app.models.raw_materials_model import RawMaterials
from app.models.supplier_model import Supplier
from app.models.purchase_request_model import PurchaseRequest
from app.seeds.user_seeds import users_data
from app.seeds.raw_material_seeds import raw_materials_data
from app.seeds.supplier_seeds import suppliers_data
from app.seeds.purchase_request_seeds import purchase_requests_data

seed_configs = {
        "users": {
            "model": Users,
            "data": users_data,
            "fields": ["username", "division", "password"],
            "process_function": lambda session, user_data: (
                lambda user: (user.set_password(user_data["password"]), user)[1])
                (Users(username=user_data["username"], division=user_data["division"]))
        },
        "raw_materials": {
            "model": RawMaterials,
            "data": raw_materials_data,
            "fields": ["name", "type", "brand", "purchase_unit", "quantity", "quantity_unit"],
            "process_function": lambda session, raw_material_data: RawMaterials(
                name=raw_material_data["name"],
                type=raw_material_data["type"],
                brand=raw_material_data["brand"],
                purchase_unit=raw_material_data["purchase_unit"],
                quantity=raw_material_data["quantity"],
                quantity_unit=raw_material_data["quantity_unit"]
            )
        },
        "suppliers": {
            "model": Supplier,
            "data": suppliers_data,
            "fields": ["name", "address", "phone_number"],
            "process_function": lambda session, supplier_data: Supplier(
                name=supplier_data["name"],
                address=supplier_data["address"],
                phone_number=supplier_data["phone_number"]
            )
        },
        "purchase_requests": {
            "model": PurchaseRequest,
            "data": purchase_requests_data,
            "fields": ["pr_code","user_id","division","raw_material_id", "quantity"],
            "process_function": lambda session, purchase_request_data: PurchaseRequest(
                pr_code=purchase_request_data["pr_code"],
                user_id=purchase_request_data["user_id"],
                division=purchase_request_data["division"],
                raw_material_id=purchase_request_data["raw_material_id"],
                quantity=purchase_request_data["quantity"]
            )
        }
    }