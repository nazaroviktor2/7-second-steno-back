
from pydantic import BaseModel, Field

from app.schemas.order_schemas import BaseOrder


class UserOrdersIn(BaseModel):
    offset: int = 0
    limit: int = 20


class UserOrdersOut(BaseModel):
    user_id: str = Field(description="id пользователя")
    orders: list[BaseOrder] = Field(description="Заказы пользователя")


