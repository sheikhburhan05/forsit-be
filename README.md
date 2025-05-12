This is a FastAPI-based backend API designed to power a web admin dashboard for e-commerce managers. It provides endpoints for analyzing sales, tracking revenue, managing inventory, and registering new products. The API is built with Python, FastAPI, SQLAlchemy, and connects to a MySQL database hosted on Aiven.

## Setup Instructions

### Prerequisites
- Python 3.13
- Docker (optional, for containerized deployment)
- Git
- Access to the Aiven MySQL database (connection details in `.env`)

### Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/sheikhburhan05/forsit-be.git
   cd project
   ```

2. **Install Dependencies**:
   Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**:
   Create a `.env` file in the project root and add the Aiven MySQL connection string:
   ```
   DATABASE_URL=''
   ```

4. **Create Database Tables**:
   Run the application to initialize the database tables:
   ```bash
   python -m uvicorn src.main:app --host 0.0.0.0 --port 8000
   ```
   The tables (`products`, `inventory`, `sales`) will be created in the `defaultdb` database.

5. **Seed Demo Data**:
   Populate the database with sample data for testing:
   ```bash
   python src/scripts/seed_data.py
   ```

6. **Run the Application**:
   Start the FastAPI server using Docker or directly:
   - **With Docker**:
     ```bash
     docker-compose up -d
     ```
   - **Without Docker**:
     ```bash
     python -m uvicorn src.main:app --host 0.0.0.0 --port 8000
     ```

7. **Access the API**:
   - Interactive API documentation: `http://localhost:8000/docs`
   - API endpoints: `http://localhost:8000/api/v1`

### Dependencies
The project dependencies are listed in `requirements.txt`:
```
fastapi==0.115.0
uvicorn==0.30.6
sqlalchemy==2.0.35
pymysql==1.1.1
python-dotenv==1.0.1
pydantic==2.9.2
```

These include:
- **FastAPI**: Web framework for building the API.
- **Uvicorn**: ASGI server for running the API.
- **SQLAlchemy**: ORM for database interactions.
- **PyMySQL**: MySQL driver for SQLAlchemy.
- **python-dotenv**: For loading environment variables.
- **Pydantic**: For data validation and serialization.

## API Endpoints

The API provides endpoints under the `/api/v1` prefix, organized by functionality. All endpoints are documented in the interactive Swagger UI at `http://localhost:8000/docs`.

### Sales
- **GET /api/v1/sales**
  - **Description**: Retrieves sales data with optional filters for date range, product, and category.
  - **Query Parameters**:
    - `start_date`: ISO datetime (e.g., `2025-01-01T00:00:00`) - Filter sales from this date.
    - `end_date`: ISO datetime - Filter sales up to this date.
    - `product_id`: Integer - Filter sales for a specific product.
    - `category`: String - Filter sales by product category.
    - `skip`: Integer (default: 0) - Skip records for pagination.
    - `limit`: Integer (default: 100) - Limit records returned.
  - **Response**: List of sales records with `id`, `product_id`, `quantity`, `total_price`, and `sale_date`.

### Revenue
- **GET /api/v1/revenue**
  - **Description**: Analyzes revenue by period (daily, weekly, monthly, yearly) with optional filters.
  - **Query Parameters**:
    - `period`: String (default: `daily`) - Group revenue by `daily`, `weekly`, `monthly`, or `yearly`.
    - `start_date`: ISO datetime - Filter revenue from this date.
    - `end_date`: ISO datetime - Filter revenue up to this date.
    - `category`: String - Filter revenue by product category.
  - **Response**: List of objects with `period` (truncated date) and `total_revenue` (sum of `total_price`).

### Inventory
- **GET /api/v1/inventory**
  - **Description**: Retrieves current inventory status, with an option to filter low-stock items.
  - **Query Parameters**:
    - `low_stock`: Boolean (default: `false`) - If `true`, returns only items where `quantity <= low_stock_threshold`.
  - **Response**: List of inventory records with `id`, `product_id`, `quantity`, `low_stock_threshold`, and `last_updated`.
- **PATCH /api/v1/inventory/{inventory_id}**
  - **Description**: Updates the quantity of an inventory item.
  - **Path Parameter**:
    - `inventory_id`: Integer - ID of the inventory record.
  - **Body**:
    ```json
    { "quantity": 50 }
    ```
  - **Response**: Updated inventory record.

### Products
- **POST /api/v1/products**
  - **Description**: Registers a new product.
  - **Body**:
    ```json
    {
      "name": "Laptop",
      "category": "Electronics",
      "price": 999.99
    }
    ```
  - **Response**: Created product with `id`, `name`, `category`, and `price`.

## Additional Notes
- **Database Documentation**: See `DATABASE.md` for detailed information on the database schema, tables, relationships, and indexes.
- **Demo Data**: The `seed_data.py` script populates the database with sample products, inventory, and sales data for testing.