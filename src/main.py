from fastapi import FastAPI
from src.api.v1 import sales, revenue, inventory, products
from src.database.config import engine
from src.database import models
import uvicorn

app = FastAPI(title="E-commerce Admin API", version="1.0.0")

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Include API routers
app.include_router(sales.router, prefix="/api/v1", tags=["Sales"])
app.include_router(revenue.router, prefix="/api/v1", tags=["Revenue"])
app.include_router(inventory.router, prefix="/api/v1", tags=["Inventory"])
app.include_router(products.router, prefix="/api/v1", tags=["Products"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)