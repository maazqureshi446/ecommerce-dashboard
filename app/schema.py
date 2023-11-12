from pydantic import BaseModel


class SalesSchema(BaseModel):
    product_id: int
    name: str
    quantity: int
    amount: float
    discount: float
    total: float
    sale_date: str


class RevenueSchema(BaseModel):
    revenue: float
    display_date: str


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    category_id: int


class InventoryResponse(BaseModel):
    product_id: int
    product_name: str
    current_quantity: int
    low_stock_alert: bool


class InventoryCreate(BaseModel):
    product_id: int
    quantity: int
