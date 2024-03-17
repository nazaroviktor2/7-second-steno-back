from fastapi import APIRouter, Depends

from app.api.v1.endpoints.auth import get_current_user
from app.db.db_crud import get_all_user_orders
from app.schemas.order_schemas import BaseOrder
from app.schemas.user_schemas import UserOrdersIn, UserOrdersOut

router = APIRouter()


@router.get("/orders")
async def get_user_orders(payload: UserOrdersIn = Depends(), user=Depends(get_current_user)) -> UserOrdersOut:
    orders = await get_all_user_orders()
    orders = [
        BaseOrder(
            order_id=str(order.id),
            status=order.status,
            preview=order.preview,
            name=order.name
        )
        for order in orders
    ]
    return UserOrdersOut(user_id=user.id, orders=orders)
