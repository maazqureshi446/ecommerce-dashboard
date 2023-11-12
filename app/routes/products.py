from typing import Any
from fastapi import APIRouter, HTTPException
from fastapi_sqlalchemy import db
from starlette.responses import JSONResponse

from app.models import Product, ProductCategory
from app.schema import ProductCreate


class ProductRouter:
    @property
    def router(self):
        api_router = APIRouter(prefix="/api", tags=["Products"])

        @api_router.post("/addProduct", status_code=201)
        def add_product(product_data: ProductCreate) -> Any:
            category = db.session.query(ProductCategory).get(product_data.category_id)
            if not category:
                raise HTTPException(status_code=404, detail="Category not found")

            new_product = Product(
                name=product_data.name,
                description=product_data.description,
                price=product_data.price,
                category_id=product_data.category_id
            )

            db.session.add(new_product)
            db.session.commit()

            return JSONResponse(content={"message": "Product added successfully"}, status_code=201)

        return api_router
