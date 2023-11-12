from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, func
from sqlalchemy.orm import relationship, column_property
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# Parent table with common fields
class BaseTable(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())


class User(BaseTable):
    __tablename__ = 'users'

    username = Column(String(32), unique=True, index=True, nullable=False)
    password = Column(String(64), nullable=False)

    inventory = relationship("Inventory", back_populates="user")


class ProductCategory(BaseTable):
    __tablename__ = 'product_categories'

    name = Column(String(32), unique=True, index=True, nullable=False)

    product = relationship("Product", back_populates="category")


class Product(BaseTable):
    __tablename__ = 'products'

    name = Column(String(32), index=True, nullable=False)
    description = Column(String(64))
    price = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey('product_categories.id'))

    category = relationship("ProductCategory", back_populates="product")
    sales = relationship("Sale", back_populates="product")
    inventory = relationship("Inventory", back_populates="product")


class Sale(BaseTable):
    __tablename__ = 'sales'

    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    discount = Column(Float)
    total = column_property(amount - discount)
    sale_date = Column(DateTime, nullable=False)

    product = relationship("Product", back_populates="sales")


class Inventory(BaseTable):
    __tablename__ = 'inventory'

    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer, nullable=False)
    date_added = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    product = relationship("Product", back_populates="inventory")
    user = relationship("User", back_populates="inventory")
