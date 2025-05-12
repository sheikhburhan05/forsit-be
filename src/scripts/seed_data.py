from sqlalchemy.orm import Session
from src.database.config import SessionLocal
from src.database.models import Product, Inventory, Sale
from datetime import datetime, timedelta
import random


def seed_data():
    db = SessionLocal()
    try:
        # Sample products
        products = [
            Product(name="Laptop", category="Electronics", price=999.99),
            Product(name="Smartphone", category="Electronics", price=599.99),
            Product(name="T-shirt", category="Clothing", price=19.99),
            Product(name="Jeans", category="Clothing", price=49.99),
        ]
        db.add_all(products)
        db.commit()

        # Sample inventory
        inventories = [
            Inventory(
                product_id=p.id,
                quantity=random.randint(20, 100),
                low_stock_threshold=10,
            )
            for p in products
        ]
        db.add_all(inventories)
        db.commit()

        # Sample sales
        start_date = datetime(2025, 1, 1)
        sales = []
        for _ in range(100):
            product = random.choice(products)
            quantity = random.randint(1, 5)
            sales.append(
                Sale(
                    product_id=product.id,
                    quantity=quantity,
                    total_price=product.price * quantity,
                    sale_date=start_date + timedelta(days=random.randint(0, 90)),
                )
            )
        db.add_all(sales)
        db.commit()

    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
