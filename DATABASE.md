# Database Documentation

This document describes the database schema for the E-commerce Admin API, which powers a web admin dashboard for e-commerce managers. The schema is implemented in MySQL (hosted on Aiven) and uses SQLAlchemy for ORM. It is designed to support sales analysis, revenue tracking, inventory management, and product registration. The schema is normalized to the third normal form (3NF) to prevent redundancy and ensure consistency, with optimized indexes for query performance.

## Tables

### 1. products

- **Purpose**: Stores product information, including name, category, and price, serving as the central entity for inventory and sales.
- **Columns**:
  - `id`: Integer (Primary Key) - Unique identifier for each product.
  - `name`: String(100), Unique - Product name (e.g., "Laptop").
  - `category`: String(50) - Product category (e.g., "Electronics").
  - `price`: Float - Product price (e.g., 999.99).
- **Relationships**:
  - One-to-Many with `inventory`: Each product has one inventory record.
  - One-to-Many with `sales`: Each product can have multiple sales records.
- **Indexes**:
  - Primary Key: `id`
  - Index: `category` (ix_products_category) - Optimizes category-based queries in sales and revenue endpoints.
  - Unique Constraint: `name` (uq_products_name) - Prevents duplicate product names.

### 2. inventory

- **Purpose**: Tracks inventory levels for each product, including stock quantity and low-stock alerts, supporting inventory management features.
- **Columns**:
  - `id`: Integer (Primary Key) - Unique identifier for each inventory record.
  - `product_id`: Integer (Foreign Key to `products`, ondelete=CASCADE) - References the associated product.
  - `quantity`: Integer - Current stock quantity.
  - `low_stock_threshold`: Integer - Threshold for low-stock alerts (default: 10).
  - `last_updated`: DateTime - Timestamp of the last inventory update.
- **Relationships**:
  - Many-to-One with `products`: Each inventory record belongs to one product.
- **Indexes**:
  - Primary Key: `id`
  - Index: `product_id` - Optimizes joins with `products`.
  - Composite Index: `(product_id, quantity)` (ix_inventory_product_quantity) - Optimizes low-stock queries with joins.

### 3. sales

- **Purpose**: Records sales transactions, including quantity sold, total price, and sale date, enabling sales and revenue analysis.
- **Columns**:
  - `id`: Integer (Primary Key) - Unique identifier for each sale.
  - `product_id`: Integer (Foreign Key to `products`, ondelete=CASCADE) - References the sold product.
  - `quantity`: Integer - Number of units sold.
  - `total_price`: Float - Total sale amount (quantity \* price at time of sale).
  - `sale_date`: DateTime - Date and time of the sale.
- **Relationships**:
  - Many-to-One with `products`: Each sale is associated with one product.
- **Indexes**:
  - Primary Key: `id`
  - Index: `product_id` - Optimizes joins with `products`.
  - Index: `sale_date` - Optimizes date range queries for sales and revenue.
  - Composite Index: `(sale_date, product_id)` (ix_sales_date_product) - Optimizes sales filtering by date and product.

## Design Notes

- **Normalization**:
  - The schema is in 3NF, ensuring no redundancy in product details, inventory, or sales data.
  - A minor denormalization exists in `sales.total_price`, which stores the sale amount to preserve historical prices (e.g., if `products.price` changes). This improves performance for revenue calculations by avoiding joins.
- **Consistency**:
  - Foreign keys (`product_id` in `inventory` and `sales`) with `ondelete=CASCADE` ensure that deleting a product removes its associated `inventory` and `sales` records, preventing orphaned data.
  - The unique constraint on `products.name` prevents duplicate products.
- **Performance**:
  - Indexes are optimized for common API query patterns:
    - `products.category` for filtering sales and revenue by category.
    - `sales.sale_date` and `(sale_date, product_id)` for date range and product-specific sales queries.
    - `inventory.product_id, quantity` for low-stock checks with joins.
  - Indexes are minimal to balance read and write performance.
- **Relationships**:
  - Defined using SQLAlchemy `relationship` for efficient querying (e.g., joining `sales` with `products` for category data).
  - Enforced via foreign keys to maintain referential integrity.
- **Support for API**:
  - **Sales**: The `sales` table supports filtering by `sale_date`, `product_id`, and `category` (via `products` join).
  - **Revenue**: `sales.total_price` and `sale_date` enable period-based aggregations, with `products.category` for category filtering.
  - **Inventory**: The `inventory` table supports quantity updates and low-stock alerts.
  - **Products**: The `products` table supports new product registration with unique names.

## Verification

- **Table Creation**: Run the application (`python -m uvicorn src.main:app`) to create tables in the Aiven `defaultdb` database.
- **Index Verification**: Connect to the Aiven MySQL database and run:
  ```sql
  SHOW TABLES;
  SHOW INDEX FROM products;
  SHOW INDEX FROM inventory;
  SHOW INDEX FROM sales;
  ```
- **Demo Data**: Use `python src/scripts/seed_data.py` to populate the database with sample data for testing.

For additional details on the database configuration, see `src/database/models.py` and `src/database/config.py`.
