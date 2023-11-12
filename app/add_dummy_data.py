import os
import random
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from models import Base, User, ProductCategory, Product, Sale, Inventory

load_dotenv()


def add_dummy_data():
    DATABASE_URL = os.environ["DATABASE_URL"]
    engine = create_engine(DATABASE_URL)

    Base.metadata.bind = engine

    Session = sessionmaker(bind=engine)
    session = Session()

    users_data = [
        {"username": "john_doe", "password": "password123"},
        {"username": "jane_doe", "password": "securepass"},
        {"username": "alice_smith", "password": "mysecretpass"},
        {"username": "bob_jones", "password": "letmein"},
        {"username": "emily_davis", "password": "strongpassword"},
    ]

    for user_data in users_data:
        user = User(**user_data)
        session.add(user)

    categories_data = [
        {"name": "Electronics"},
        {"name": "Clothing"},
        {"name": "Home Appliances"},
        {"name": "Books"},
        {"name": "Sports and Outdoors"},
    ]

    for category_data in categories_data:
        category = ProductCategory(**category_data)
        session.add(category)

    products_data = [
        {"name": "Smartphone", "description": "Latest smartphone model", "price": 599.99, "category_id": 1},
        {"name": "Laptop", "description": "High-performance laptop", "price": 1299.99, "category_id": 1},
        {"name": "T-shirt", "description": "Comfortable cotton T-shirt", "price": 19.99, "category_id": 2},
        {"name": "Refrigerator", "description": "Energy-efficient refrigerator", "price": 899.99, "category_id": 3},
        {"name": "Sci-fi Book", "description": "Bestseller sci-fi novel", "price": 24.99, "category_id": 4},
        {"name": "Running Shoes", "description": "Durable running shoes", "price": 79.99, "category_id": 5},
    ]

    for product_data in products_data:
        product = Product(**product_data)
        session.add(product)

    sales_data = []
    for product_id in range(1, 6):
        quantity = random.randint(1, 10)
        amount = product_id * 20.0 + random.uniform(5.0, 15.0)  # Variation in amount
        discount = random.uniform(0.0, 10.0)
        sale_date = datetime.now() - timedelta(days=random.randint(1, 30))
        sale = Sale(product_id=product_id, quantity=quantity, amount=amount, sale_date=sale_date, discount=discount)
        sales_data.append(sale)

    for sale_data in sales_data:
        session.add(sale_data)

    inventory_data = []
    for product_id in range(1, 6):
        for user_id in range(1, 6):
            quantity = random.randint(50, 100)
            date_added = datetime.now() - timedelta(days=random.randint(1, 365))
            inventory_item = Inventory(product_id=product_id, quantity=quantity, date_added=date_added, user_id=user_id)
            inventory_data.append(inventory_item)

    for inventory_item_data in inventory_data:
        session.add(inventory_item_data)

    session.commit()
    session.close()


if __name__ == '__main__':
    add_dummy_data()
