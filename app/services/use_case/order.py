from uuid import UUID

from app.db.db_crud import get_order_by_id
from app.db.models import Order


async def service_get_order(order_id: UUID) -> Order:
    """Возвращает заказ."""
    return await get_order_by_id(str(order_id))
