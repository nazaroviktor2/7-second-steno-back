from enum import Enum
from uuid import UUID

from fastapi import UploadFile
from pydantic import BaseModel, Field


# from app.schemas.models import MetaFileDTO

class OrderStatus(Enum):
    in_queue: str = "В очереди"
    in_process: str = "В работе"


class BaseOrder(BaseModel):
    order_id: str = Field(description="id заказа")
    status: OrderStatus = Field(description="статут заказа", default=OrderStatus.in_queue)
    short_description: str = Field(description="краткое описание", default="краткое описание")
    name: str = Field(description="название", default="название 1")


# class MetaFileGetOut(MetaFileDTO):
#     pass
