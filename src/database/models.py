from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    Index,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from .config import Base
from datetime import datetime


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    category = Column(String(50), nullable=False, index=True)
    price = Column(Float, nullable=False)
    inventory = relationship(
        "Inventory", back_populates="product", cascade="all, delete"
    )
    sales = relationship("Sale", back_populates="product", cascade="all, delete")

    __table_args__ = (
        Index("ix_products_category", "category"),
        UniqueConstraint("name", name="uq_products_name"),
    )


class Inventory(Base):
    __tablename__ = "inventory"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(
        Integer, ForeignKey("products.id", ondelete="CASCADE"), index=True
    )
    quantity = Column(Integer, nullable=False)
    low_stock_threshold = Column(Integer, default=10)
    last_updated = Column(DateTime, default=datetime.utcnow)
    product = relationship("Product", back_populates="inventory")

    __table_args__ = (Index("ix_inventory_product_quantity", "product_id", "quantity"),)


class Sale(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(
        Integer, ForeignKey("products.id", ondelete="CASCADE"), index=True
    )
    quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    sale_date = Column(DateTime, default=datetime.utcnow, index=True)
    product = relationship("Product", back_populates="sales")

    __table_args__ = (Index("ix_sales_date_product", "sale_date", "product_id"),)
