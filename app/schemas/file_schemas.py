from uuid import UUID

from fastapi import UploadFile
from pydantic import BaseModel, Field

# from app.schemas.models import MetaFileDTO


class UploadFileIn(BaseModel):
    file: UploadFile = Field(description="Файл для обработки")
    priority: bool = False


class UploadFileOut(BaseModel):
    message: str = Field(description="Сообщение от сервера")
    order: str = Field(description="Номер созданного заказа")


# class MetaFileGetOut(MetaFileDTO):
#     pass
