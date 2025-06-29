from typing import List

import uvicorn
from fastapi import FastAPI, Depends, Query, HTTPException
from fastapi.responses import RedirectResponse

from sqlalchemy import select, and_, or_, desc, asc, func
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

from backend.parser.WB import WB
from backend.parser.db import ProductCard, engine, SessionLocal

from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Page, add_pagination, Params

from backend.parser.dto import ProductCardDTO


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()

add_pagination(app)

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],

)


@app.get("/")
async def root():
    return RedirectResponse("/api/products")


@app.get("/api/products/rangeValue")
async def get_products(value: str, db: Session = Depends(get_db)):
    allowed_order_fields = {
        # "name": ProductCard.name,
        "price": ProductCard.price,
        "sale_price": ProductCard.sale_price,
        "rating": ProductCard.rating,
        "review_count": ProductCard.review_count,
    }

    result = select(
        func.max(allowed_order_fields.get(value)).label("max_value"),
        func.min(allowed_order_fields.get(value)).label("min_value")
    )

    result = db.execute(result).first()

    return {
        "max_value": result.max_value,
        "min_value": result.min_value
    }


@app.get("/api/run_parser")
async def get_run_parser(url: str):

    if "www" not in url or "http" not in url:
        return HTTPException(status_code=404, detail="Неверная ссылка.")

    wb = WB(user_input=url)
    wb.run()
    try:
        wb.run()
        return {"success": True}
    except Exception as e:
        print(e)
        return {"success": False,
                "message": str(e)}


@app.get("/api/products")
async def get_products(
        # page: int = 1,
        min_price: float = Query(default=0.0, description="Минимальная цена", ge=0.0, ),
        max_price: float = Query(default=69087.15, description="Максимальная цена", ge=0.0),
        rating_from: float = Query(default=0.0, description="Показать с рейтингом выше чем", ge=0.0, le=5.0),
        min_review_count: int = Query(default=0, description="Минимальное количество отзывов", ge=0.0),
        # max_review_count: int = Query(default=10000, description="Максимальное количество отзывов", ge=0.0),
        order_by: str = "name",
        is_statistic:bool = False,
        db: SessionLocal = Depends(get_db),
        params: Params = Depends(),
)->Page[ProductCardDTO] | List[ProductCardDTO]:
    allowed_order_fields = {
        "name": ProductCard.name,
        "price": ProductCard.price,
        "sale_price": ProductCard.sale_price,
        "rating": ProductCard.rating,
        "review_count": ProductCard.review_count,
    }

    if order_by.startswith("-"):
        field_name = order_by[1:]
        order_column = allowed_order_fields.get(field_name)
        order_by = desc(order_column) if order_column else asc(ProductCard.name)
    else:
        order_column = allowed_order_fields.get(order_by)
        order_by = asc(order_column) if order_column else asc(ProductCard.name)
    slt = select(ProductCard).where(
        and_(
            or_(
                and_(ProductCard.price >= min_price, ProductCard.price <= max_price),
                and_(ProductCard.sale_price >= min_price, ProductCard.sale_price <= max_price),
            ),
            ProductCard.rating >= rating_from,
            ProductCard.review_count >= min_review_count,

        )

    ).order_by(order_by)
    if not is_statistic:
        return  paginate(db, slt, params)

    return db.execute(slt).scalars().all()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
