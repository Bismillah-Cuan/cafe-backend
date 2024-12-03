# init_db.py
from app.connections.db import engine, Base
from app.models.users_model import Users  # Mengimpor model dari models.py
from app.models.raw_materials_model import RawMaterials
from app.models.supplier_model import Supplier
from app.models.stock_inventory_model import StockInventory

# Membuat semua tabel yang belum ada berdasarkan model
Base.metadata.create_all(engine)

print("All tables created")
