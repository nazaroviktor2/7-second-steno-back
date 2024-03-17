from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.database import async_session_factory
from app.db.models import Order, OrderStatus
from app.services.exceptions import OrderNotFoundError


async def get_order_by_id(order_id: str) -> Order:
    """Возвращать заказ по order_id."""
    order_id = UUID(order_id)

    async with async_session_factory() as session:
        order = await session.get(Order, order_id)
        if not order:
            raise OrderNotFoundError(order_id)
    return order


async def create_new_order(name: str) -> UUID:
    """Создает новый заказ в базе данных.

    Returns
    -------
    UUID
        Идентификатор созданного заказа.
    """
    async with async_session_factory() as session:
        order = Order(name=name)
        session.add(order)
        await session.commit()
    return order.id


async def order_add_minio_path(order_id: str, minio_path: str) -> UUID:
    """Создает новый заказ в базе данных.

    Returns
    -------
    UUID
        Идентификатор созданного заказа.
    """
    order_id = UUID(order_id)
    async with async_session_factory() as session:
        order = await session.get(Order, order_id)
        if not order:
            raise OrderNotFoundError(order_id)
        order.minio_path = minio_path

        await session.commit()
    return order.id


async def order_add_preview(order_id: str, preview: str) -> UUID:
    """Создает новый заказ в базе данных.

    Returns
    -------
    UUID
        Идентификатор созданного заказа.
    """
    order_id = UUID(order_id)

    async with async_session_factory() as session:
        order = await session.get(Order, order_id)
        if not order:
            raise OrderNotFoundError(order_id)
        order.preview = preview

        await session.commit()
    return order.id


async def order_set_status(order_id: str, status: OrderStatus) -> UUID:
    """Создает новый заказ в базе данных.

    Returns
    -------
    UUID
        Идентификатор созданного заказа.
    """
    order_id = UUID(order_id)

    async with async_session_factory() as session:
        order = await session.get(Order, order_id)
        if not order:
            raise OrderNotFoundError(order_id)
        order.status = status

        await session.commit()
    return order.id


async def get_all_user_orders(user_id: str=None, skip: int =0, limit: int=20):
    async with async_session_factory() as session:
        query = await session.scalars(select(Order).offset(skip).limit(limit))

    return query.all()
