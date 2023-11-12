# E-commerce Store Database Schema

## User Table

- **Purpose:**
  - Represents users who have accounts in the e-commerce system.
  - Used for authentication and authorization.
- **Columns:**
  - **username:** Unique identifier for each user.
  - **password:** Securely stores the password for user authentication.
- **Relationships:**
  - **inventory:** Tracks the inventory records associated with a user. Allows for a history of the products a user has interacted with.

## ProductCategory Table

- **Purpose:**
  - Represents different categories of products available in the e-commerce system.
- **Columns:**
  - **name:** Unique identifier for each product category.
- **Relationships:**
  - **product:** Establishes a relationship with the Product table, allowing multiple products to belong to a single category.

## Product Table

- **Purpose:**
  - Represents individual products available for purchase.
- **Columns:**
  - **name:** Unique identifier for each product.
  - **description:** Provides additional information about the product.
  - **price:** Indicates the price of the product.
  - **category_id:** Links the product to a specific category.
- **Relationships:**
  - **category:** Links the product to a product category.
  - **sales:** Tracks the sales records associated with a product.
  - **inventory:** Tracks the inventory records associated with a product.

## Sale Table

- **Purpose:**
  - Records individual sales transactions.
- **Columns:**
  - **product_id:** Links the sale to a specific product.
  - **quantity:** Indicates the quantity of the product sold.
  - **amount:** Represents the total amount of the sale before any discounts.
  - **discount:** Represents any discount applied to the sale.
  - **total:** Computed column representing the total amount after applying the discount.
  - **sale_date:** Records the date and time of the sale.
- **Relationships:**
  - **product:** Establishes a relationship with the Product table, linking each sale to a specific product.

## Inventory Table

- **Purpose:**
  - Tracks the quantity of each product available in the inventory.
- **Columns:**
  - **product_id:** Links the inventory record to a specific product.
  - **quantity:** Indicates the quantity of the product in the inventory.
  - **date_added:** Records the date and time when the product was added to the inventory.
  - **user_id:** Links the inventory record to a specific user.
- **Relationships:**
  - **product:** Establishes a relationship with the Product table, linking each inventory record to a specific product.
  - **user:** Links the inventory record to a specific user.
