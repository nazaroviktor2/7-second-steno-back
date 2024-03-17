from fastapi import APIRouter, Depends, status, HTTPException
from loguru import logger

from app.api.v1.endpoints.auth import get_current_user
from app.db.db_crud import get_order_by_id
from app.db.models import OrderStatus
from app.schemas.order_schemas import BaseOrder, OrderWithText
from app.services.exceptions import handle_domain_error
from app.services.use_case.index import get_file_by_id

router = APIRouter()


@router.get(
    "/{order_id}",
    status_code=status.HTTP_200_OK,
    response_model=BaseOrder,
)
@handle_domain_error
async def get_order(order_id: str, user=Depends(get_current_user)):
    order = await get_order_by_id(order_id)
    return BaseOrder(
        order_id=str(order.id),
        status=order.status,
        preview=order.preview,
        name=order.name
    )


@router.get(
    "/{order_id}/text",
    status_code=status.HTTP_200_OK,
    response_model=OrderWithText,
)
@handle_domain_error
async def get_order(order_id: str, user=Depends(get_current_user)):
    order = await get_order_by_id(order_id)
    if order.status != OrderStatus.done:
        raise HTTPException(status_code=status.HTTP_425_TOO_EARLY, detail="Заказ еще обрабатывается")
    file = get_file_by_id(order_id)
    text = "Какое то текст"
    highlights = ["Сделай ....", "Выполни ..."]
    persons = ["Ваня В", "Кирилл", "Дмитрий"]
    if file:
        file = file[0]
        source = file["_source"]
        text = source.get("content")
        persons = source.get('persons')
        highlights = file.get("highlight")
        if highlights:
            highlights = highlights['content']

    return OrderWithText(
        order_id=str(order_id),
        name=order.name,
        preview=order.preview,
        status=order.status,
        text=text,
        highlights=highlights,
        persons=persons
    )
