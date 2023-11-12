from datetime import datetime
from enum import Enum
from typing import List, Any
from fastapi import APIRouter, Query
from fastapi_sqlalchemy import db
from sqlalchemy import func

from app.models import Sale, Product
from app.schema import SalesSchema, RevenueSchema


class AnalysisMode(str, Enum):
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"
    annual = "annual"


class SalesRouter:
    @property
    def router(self):
        api_router = APIRouter(prefix="/api", tags=["Sales"])

        @api_router.get("/sales", status_code=200, response_model=List[SalesSchema])
        def get_total_sale(
                product_id: int = Query(None, title="Product ID", description="Filter by product ID"),
                category_id: int = Query(None, title="Category ID", description="Filter by category ID"),
                start_date: int = Query(None, title="Start Date", description="Filter by start date (timestamp)"),
                end_date: int = Query(None, title="End Date", description="Filter by end date (timestamp)"),
                limit: int = 10, offset: int = 0) -> Any:

            start_date = datetime.utcfromtimestamp(start_date) if start_date else None
            end_date = datetime.utcfromtimestamp(end_date) if end_date else None

            query = db.session.query(Sale.product_id, Sale.quantity, Sale.amount, Sale.discount, Sale.total,
                                     Sale.sale_date, Product.name)
            query = query.join(Sale.product)

            if product_id:
                query = query.filter(Sale.product_id == product_id)

            if category_id:
                query = query.filter(Product.category_id == category_id)

            if start_date:
                query = query.where(Sale.sale_date >= start_date)

            if end_date:
                query = query.where(Sale.sale_date <= end_date)

            query = query.limit(limit).offset(offset)
            results = query.all()

            # print(results)

            resp = []
            row: Sale
            for row in results:
                resp.append({
                    'product_id': row.product_id,
                    'name': row.name,
                    'quantity': row.quantity,
                    'amount': row.amount,
                    'discount': row.discount,
                    'total': row.total,
                    'sale_date': row.sale_date.strftime('%d-%m-%Y'),
                })

            return resp

        @api_router.get("/getRevenue", status_code=200, response_model=List[RevenueSchema])
        async def total_revenue(
                mode: AnalysisMode = Query(..., title="Analysis Mode",
                                           description="Analysis mode: daily, weekly, monthly, annual"),
                start_date: int = Query(None, title="Start Date", description="Filter by start date (timestamp)"),
                end_date: int = Query(None, title="End Date", description="Filter by end date (timestamp)"),
                category_id: int = Query(None, title="Category ID", description="Filter by category ID"),
        ):
            start_date = datetime.utcfromtimestamp(start_date) if start_date else None
            end_date = datetime.utcfromtimestamp(end_date) if end_date else None

            if mode == "daily":
                date_format = "%Y-%m-%d"
            elif mode == "weekly":
                date_format = "%Y %V Week"
            elif mode == "monthly":
                date_format = "%Y-%m"
            elif mode == "annual":
                date_format = "%Y"

            query = db.session.query(func.sum(Sale.amount), func.DATE_FORMAT(Sale.sale_date, date_format))

            if mode == "daily":
                query = query.group_by(func.DATE_FORMAT(Sale.sale_date, date_format))
            elif mode == "weekly":
                query = query.group_by(func.DATE_FORMAT(Sale.sale_date, date_format))
            elif mode == "monthly":
                query = query.group_by(func.DATE_FORMAT(Sale.sale_date, date_format))
            elif mode == "annual":
                query = query.group_by(func.DATE_FORMAT(Sale.sale_date, date_format))

            if start_date:
                query = query.where(Sale.sale_date >= start_date)

            if end_date:
                query = query.where(Sale.sale_date <= end_date)

            if category_id:
                query = query.join(Sale.product).filter(Product.category_id == category_id)

            result = query.all()
            print(result)

            resp = []
            for row in result:
                resp.append({
                    'revenue': row[0],
                    'display_date': row[1]
                })

            return resp

        return api_router
