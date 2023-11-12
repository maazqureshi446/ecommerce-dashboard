import os
from fastapi import FastAPI
from dotenv import load_dotenv

from app.routes.inventory import InventoryRouter
from app.routes.sales import SalesRouter
from app.routes.products import ProductRouter
from fastapi_sqlalchemy import DBSessionMiddleware

load_dotenv()

print(os.environ["DATABASE_URL"])

app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])

sales_router = SalesRouter()
app.include_router(sales_router.router)

product_router = ProductRouter()
app.include_router(product_router.router)

inventory_router = InventoryRouter()
app.include_router(inventory_router.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
