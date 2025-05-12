from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from typing import Optional
from src.database.models import Sale, Product
from src.api.deps import get_db_session

router = APIRouter()

@router.get("/revenue")
def get_revenue(
    db: Session = Depends(get_db_session),
    period: str = "daily",
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    category: Optional[str] = None
):
    query = db.query(
        func.date_trunc(period, Sale.sale_date).label("period"),
        func.sum(Sale.total_price).label("total_revenue")
    )
    if start_date:
        query = query.filter(Sale.sale_date >= start_date)
    if end_date:
        query = query.filter(Sale.sale_date <= end_date)
    if category:
        query = query.join(Product).filter(Product.category == category)
    query = query.group_by(func.date_trunc(period, Sale.sale_date))
    return query.all()