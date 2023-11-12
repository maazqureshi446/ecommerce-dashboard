# E-commerce Dashboard

## Overview

This repository contains the source code for an E-commerce Dashboard implemented using FastAPI, SQLAlchemy, and MySQL. The dashboard provides various endpoints to retrieve, filter, and analyze sales data, manage inventory, and more.

## Setup Instructions

### 1. Clone the Repository:

```bash
git clone https://github.com/maazqureshi446/ecommerce-dashboard.git
````
### 2. Navigate to the Project Directory:
```bash
cd ecommerce-dashboard
```
### 3. Start Docker Compose:
```bash
docker-compose up -d
```
This command starts the FastAPI application and a MySQL database in detached mode.

### 4. Run Database Setup Script:
```bash
docker exec -it fastapi-app python /app/app/db_setup.py
```
This command initializes the database and adds dummy data for testing purposes.

### 5. Access the FastAPI Documentation:
Open your browser and go to http://localhost:8000/docs to interact with the API using the Swagger documentation.

## Dependencies

- **FastAPI**: Web framework used for building the API.
  - **Version:** 0.104.1

- **Uvicorn**: ASGI server used for running FastAPI applications.
  - **Version:** 0.24.0

- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM) library.
  - **Version:** 1.4.30

- **FastAPI-SQLAlchemy**: Integration between FastAPI and SQLAlchemy.
  - **Version:** 0.2.1

- **Pydantic**: Data validation and settings management using Python type hints.
  - **Version:** 2.4.2

- **MySQL Connector/Python**: MySQL driver for Python.
  - **Version:** 8.0.26

- **Dotenv**: Loads environment variables from a .env file.

- **SQLAlchemy-Utils**: Additional utility functions for SQLAlchemy.
  - **Version:** 0.37.0


# E-commerce Store API Documentation

## Add Product Endpoint

### Endpoint

- **URL:** `/api/addProduct`
- **Method:** POST
- **Status Code:** 201 Created (on successful product addition)
- **Tags:** "Products" (for categorization in FastAPI documentation)

### Request Body

- **Model:** `ProductCreate`
  - **Fields:**
    - `name`: String - Name of the product.
    - `description`: String - Description of the product.
    - `price`: Float - Price of the product.
    - `category_id`: Integer - ID of the product category to which the product belongs.

### Description

The `addProduct` endpoint allows the addition of new products to the e-commerce system. Clients can send a POST request to this endpoint with the necessary information for creating a new product. The operation includes:

1. **Category Validation:**
   - Checks if the specified category ID exists in the database. If not, it returns a 404 error with the message "Category not found."

2. **Product Creation:**
   - If the category exists, a new `Product` object is created using the provided data, including name, description, price, and category ID.

3. **Database Interaction:**
   - Adds the newly created `Product` object to the database session.
   - Commits the changes to the database.

4. **Response:**
   - Returns a JSON response with a success message: {"message": "Product added successfully"}.
   - The status code is set to 201 (Created) to indicate successful product creation.

### Example Usage

To add a new product, clients send a POST request to `/api/addProduct` with the necessary product information in the request body. If the operation is successful, the server responds with a JSON message indicating that the product was added successfully.

```json
POST /api/addProduct

Request Body:
{
  "name": "Example Product",
  "description": "This is a sample product.",
  "price": 29.99,
  "category_id": 1
}

Response:
{
  "message": "Product added successfully"
}
```

## Get Total Sale Endpoint

### Endpoint

- **URL:** `/api/sales`
- **Method:** GET
- **Status Code:** 200 OK
- **Response Model:** List of [SalesSchema](#salesschema)
- **Tags:** "Sales" (for categorization in FastAPI documentation)

### Query Parameters

- `product_id`: (Optional) Integer - Filter by product ID.
- `category_id`: (Optional) Integer - Filter by category ID.
- `start_date`: (Optional) Integer - Filter by start date (timestamp).
- `end_date`: (Optional) Integer - Filter by end date (timestamp).
- `limit`: Integer - Limit the number of results (default is 10).
- `offset`: Integer - Offset for paginated results (default is 0).

### Description

The `sales` endpoint provides the ability to retrieve, filter, and analyze sales data. It allows users to filter sales data based on product ID, category ID, date range, and supports pagination.

### Example Usage

To retrieve sales data for a specific product and date range:

```http
GET /api/sales?product_id=1&start_date=1635826800&end_date=1636508400
```

## Total Revenue Endpoint

### Endpoint

- **URL:** `/api/getRevenue`
- **Method:** GET
- **Status Code:** 200 OK
- **Response Model:** List of [RevenueSchema](#revenueschema)
- **Tags:** "Sales" (for categorization in FastAPI documentation)

### Query Parameters

- `mode`: AnalysisMode - Required field specifying the analysis mode: daily, weekly, monthly, or annual.
- `start_date`: (Optional) Integer - Filter by start date (timestamp).
- `end_date`: (Optional) Integer - Filter by end date (timestamp).
- `category_id`: (Optional) Integer - Filter by category ID.

### Description

The `total_revenue` endpoint allows users to analyze revenue on a daily, weekly, monthly, or annual basis. It provides flexibility in choosing the analysis mode and supports additional filters like start date, end date, and category ID.

### Analysis Modes

- **Daily:** Revenue is grouped by day.
- **Weekly:** Revenue is grouped by week.
- **Monthly:** Revenue is grouped by month.
- **Annual:** Revenue is grouped by year.

### Example Usage

To get the total revenue on a daily basis within a specific date range:

```http
GET /api/getRevenue?mode=daily&start_date=1635826800&end_date=1636508400
```

## Get Inventory Endpoint

### Endpoint

- **URL:** `/api/getInventory`
- **Method:** GET
- **Status Code:** 200 OK
- **Response Model:** List of [InventoryResponse](#inventoryresponse)
- **Tags:** "Inventory" (for categorization in FastAPI documentation)

### Query Parameters

- `low_stock_threshold`: Integer (default: 10, min: 0) - Threshold for low stock alert.

### Description

The `get_inventory` endpoint provides information about the current inventory status for each product. It includes details such as product ID, product name, current quantity, and a low stock alert indicator based on the specified threshold.

### Response Model: InventoryResponse

- `product_id`: Integer - ID of the product.
- `product_name`: String - Name of the product.
- `current_quantity`: Integer - Current quantity of the product in inventory.
- `low_stock_alert`: Boolean - Indicates whether the product is below the low stock threshold.

### Example Usage

To retrieve the current inventory status:

```http
GET /api/getInventory?low_stock_threshold=15
```

## Update Inventory Endpoint

### Endpoint

- **URL:** `/api/updateInventory`
- **Method:** POST
- **Status Code:** 201 OK
- **Response Model:** Dictionary
- **Tags:** "Inventory" (for categorization in FastAPI documentation)

### Request Body

- **Model:** `InventoryCreate`
  - **Fields:**
    - `product_id`: Integer - ID of the product.
    - `quantity`: Integer - Quantity to update for the product.

### Description

The `updateInventory` endpoint allows bulk updating of inventory records. Clients can send a POST request to this endpoint with a list of `InventoryCreate` objects containing the product ID and the quantity to update.

### Response Model

- `message`: String - A message indicating the success of the operation.

### Example Usage

To update inventory records:

```http
POST /api/updateInventory

Request Body:
[
  {"product_id": 1, "quantity": 20},
  {"product_id": 2, "quantity": 30}
]

Response:
{
  "message": "Inventory records created successfully"
}
```
# Database Schema

For detailed information on the database schema, please refer to the "DB Documentation.md" file.
