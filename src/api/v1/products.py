from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database.models import Product
from src.schemas.products import ProductCreate, ProductResponse
from src.api.deps import get_db_session

router = APIRouter()


@router.post("/products", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db_session)):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
