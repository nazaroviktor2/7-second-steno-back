from fastapi import APIRouter, Depends

from app.api.v1.endpoints.auth import get_current_user
from app.schemas.order_schemas import BaseOrder
from app.schemas.user_schemas import UserOrdersIn, UserOrdersOut

router = APIRouter()


@router.get("/orders")
async def get_user_orders(payload: UserOrdersIn = Depends(), user=Depends(get_current_user)) -> UserOrdersOut:

    return UserOrdersOut(user_id=user.id, orders=[BaseOrder(order_id="783b6474-7d99-4bef-ae5c-02b5e9ad2485")])