from sqlalchemy import func
from typing import List, Any
from datetime import datetime
from fastapi_sqlalchemy import db
from fastapi import APIRouter, Query

from app.models import Product, Inventory
from app.schema import InventoryResponse, InventoryCreate


class InventoryRouter:
    @property
    def router(self):
        api_router = APIRouter(prefix="/api", tags=["Inventory"])

        @api_router.get("/getInventory", status_code=200, response_model=List[InventoryResponse])
        def get_inventory(low_stock_threshold: int = Query(10, ge=0)) -> Any:

            query = db.session.query(Product.id, Product.name, func.sum(Inventory.quantity))
            query = query.join(Inventory, Product.id == Inventory.product_id)
            query = query.group_by(Product.id)
            results = query.all()

            resp = []
            for product_id, product_name, current_quantity in results:
                low_stock_alert = current_quantity < low_stock_threshold
                resp.append({
                    "product_id": product_id,
                    "product_name": product_name,
                    "current_quantity": current_quantity,
                    "low_stock_alert": low_stock_alert
                })

            return resp

        @api_router.post("/updateInventory", status_code=200, response_model=dict)
        def update_inventory(inventory_records: List[InventoryCreate]) -> Any:

            for record in inventory_records:
                product = db.session.query(Product).filter_by(id=record.product_id).first()
                if product:
                    new_inventory = Inventory(
                        product_id=record.product_id,
                        quantity=record.quantity,
                        date_added=datetime.utcnow(),
                        user_id=1  # in the future, we can get user_id from session
                    )
                    db.session.add(new_inventory)

            db.session.commit()

            return {"message": "Inventory records created successfully"}

        return api_router
