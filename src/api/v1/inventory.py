from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.database.models import Inventory, Product
from src.schemas.inventory import InventoryResponse, InventoryUpdate
from src.api.deps import get_db_session

router = APIRouter()


@router.get("/inventory", response_model=List[InventoryResponse])
def get_inventory(db: Session = Depends(get_db_session), low_stock: bool = False):
    query = db.query(Inventory).join(Product)
    if low_stock:
        query = query.filter(Inventory.quantity <= Inventory.low_stock_threshold)
    return query.all()


@router.patch("/inventory/{inventory_id}", response_model=InventoryResponse)
def update_inventory(
    inventory_id: int, update: InventoryUpdate, db: Session = Depends(get_db_session)
):
    inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
    inventory.quantity = update.quantity
    inventory.last_updated = datetime.utcnow()
    db.commit()
    db.refresh(inventory)
    return inventory
