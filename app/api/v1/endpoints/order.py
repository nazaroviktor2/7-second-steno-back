from fastapi import APIRouter, Depends, status

from app.api.v1.endpoints.auth import get_current_user
from app.schemas.order_schemas import BaseOrder, OrderWithText

router = APIRouter()


@router.get(
    "/{order_id}",
    status_code=status.HTTP_200_OK,
    response_model=BaseOrder,
)
def get_order(order_id: str, user=Depends(get_current_user)):
    return BaseOrder(order_id=order_id)


@router.get(
    "/{order_id}/text",
    status_code=status.HTTP_200_OK,
    response_model=OrderWithText,
)
def get_order(order_id: str, user=Depends(get_current_user)):
    return OrderWithText(order_id=order_id)