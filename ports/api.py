from adapter.sqlalchemy_inventory import SQLAlchemyInventoryAdapter
from db import get_db
from domain.errors import InvalidQuantity, OutOfStock, UnknownSku
from domain.models import OrderRequest
from domain.use_cases import place_order
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.engine import Connection

router = APIRouter()


class PlaceOrderIn(BaseModel):
    sku: str
    qty: int = Field(..., gt=0)


class PlaceOrderOut(BaseModel):
    sku: str
    qty: int
    remaining_stock: int


# def place_order(db: Connection, sku: str, qty: int) -> dict[str, Any]:
#     """
#     😬 MIXED: domain rules + DB access + HTTP errors + response shaping.
#     """
#     if qty <= 0:
#         raise InvalidQuantity()
#         # raise HTTPException(status_code=400, detail="qty must be > 0")

#     row = db.execute(
#         text("SELECT stock FROM inventory WHERE sku=:sku"),
#         {"sku": sku},
#     ).fetchone()

#     if row is None:
#         raise UnknownSku(sku)
#         # raise HTTPException(status_code=404, detail="unknown sku")

#     available = int(row.stock)
#     if available < qty:
#         raise OutofStock(sku, qty, available)
#         # raise HTTPException(
#         #     status_code=409,
#         #     detail=f"out of stock: requested {qty}, available {available}",
#         # )

#     # Not fully atomic in a concurrent setting, but ok for demo
#     db.execute(
#         text("UPDATE inventory SET stock = stock - :qty WHERE sku=:sku"),
#         {"sku": sku, "qty": qty},
#     )
#     remaining = db.execute(
#         text("SELECT stock FROM inventory WHERE sku=:sku"),
#         {"sku": sku},
#     ).scalar_one()

#     # API response shaping in the domain-y function
#     return {"status": "ok", "sku": sku, "qty": qty, "remaining_stock": int(remaining)}


@router.post("/orders", response_model=PlaceOrderOut)
def place_order_endpoint(
    payload: PlaceOrderIn,
    connection: Connection = Depends(get_db),
) -> PlaceOrderOut:
    try:
        result = place_order(OrderRequest(**payload.model_dump()),
            SQLAlchemyInventoryAdapter(conn=connection),)
        # return PlaceOrderOut(**result)
    except InvalidQuantity as e:
        raise HTTPException(status_code=400, detail=str(e))
    except UnknownSku as e:
        raise HTTPException(status_code=404, detail=str(e))
    except OutOfStock as e:
        raise HTTPException(status_code=409, detail=str(e))

    return PlaceOrderOut(**result)