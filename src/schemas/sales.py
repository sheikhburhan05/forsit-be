from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class SaleResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    total_price: float
    sale_date: datetime

    class Config:
        orm_mode = True


class SaleFilter(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    product_id: Optional[int] = None
    category: Optional[str] = None
