from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
from src.database.models import Sale, Product
from src.schemas.sales import SaleResponse, SaleFilter
from src.api.deps import get_db_session

router = APIRouter()


@router.get("/sales", response_model=List[SaleResponse])
def get_sales(
    db: Session = Depends(get_db_session),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    product_id: Optional[int] = None,
    category: Optional[str] = None,
    skip: int = 0,
    limit: int = 20,
):
    query = db.query(Sale).join(Product)
    if start_date:
        query = query.filter(Sale.sale_date >= start_date)
    if end_date:
        query = query.filter(Sale.sale_date <= end_date)
    if product_id:
        query = query.filter(Sale.product_id == product_id)
    if category:
        query = query.filter(Product.category == category)
    return query.offset(skip).limit(limit).all()
