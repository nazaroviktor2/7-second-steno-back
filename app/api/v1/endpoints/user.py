from fastapi import APIRouter, Depends

from app.api.v1.endpoints.auth import get_current_user
from app.db.db_crud import get_all_user_orders
from app.schemas.order_schemas import BaseOrder
from app.schemas.user_schemas import UserOrdersIn, UserOrdersOut
from app.services.exceptions import handle_domain_error

router = APIRouter()


@router.get("/orders")
@handle_domain_error
async def get_user_orders(payload: UserOrdersIn = Depends(), user=Depends(get_current_user)) -> UserOrdersOut:
    orders = await get_all_user_orders(skip=payload.offset, limit=payload.limit)
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
