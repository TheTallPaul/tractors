from sqlmodel import Session, select
from app.database import Supplier, Inventory

def get_supplier_id_dict(session: Session) -> dict[int, str]:
    suppliers = session.exec(select(Supplier)).all()
    return {supplier.id: supplier.name for supplier in suppliers}

def get_inventory_dict(session: Session) -> dict[str, int]:
    inventory = session.exec(select(Inventory)).all()
    return {item.part_serial: item.quantity for item in inventory}
