from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class InventoryResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    low_stock_threshold: int
    last_updated: datetime

    class Config:
        orm_mode = True


class InventoryUpdate(BaseModel):
    quantity: int
