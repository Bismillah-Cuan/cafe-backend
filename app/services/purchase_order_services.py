from app.connections.db import Session
from app.models.purchase_order_model import PurchaseOrder
from flask import jsonify

@staticmethod
def get_all_purchase_orders():
    with Session() as session:
        purchase_orders = session.query(PurchaseOrder).all()
        return jsonify(purchase_orders)