from pydantic import BaseModel, Field

from app.db.models import OrderStatus


class BaseOrder(BaseModel):
    order_id: str = Field(description="id заказа")
    name: str = Field(description="название", default="название 1")
    status: OrderStatus = Field(description="статут заказа", default=OrderStatus.in_queue)
    preview: str = Field(description="краткое описание", default="краткое описание")


class OrderWithText(BaseOrder):
    persons: list[str] = Field(description="Имена из разговора", default=["Ваня В", "Кирилл", "Дмитрий"])
    summary: dict[str, str] = Field(description="", default="какой текст")
    text: str = Field(description="Текст", default="Какой то текст")
    highlights: list[str] = Field(description="Поручения", default=["Сделай ....", "Выполни ..."])
