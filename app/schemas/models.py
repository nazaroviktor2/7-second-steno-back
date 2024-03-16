# from datetime import datetime
# from uuid import UUID
#
# from pydantic import BaseModel, Field
#
# from app.db.models import FileStatus
#
#
# class TimesFieldMixin:
#     created_at: datetime = Field(description="Дата и время создания")
#     updated_at: datetime = Field(description="Дата и время обновления")
#
#
# class IndexDTO(BaseModel):
#     id: UUID = Field(description="Уникальный идентификатор индекса")
#     name: str = Field(description="Название индекса")
#
#
# class MetaFileDTO(BaseModel, TimesFieldMixin):
#     id: UUID = Field(description="Уникальный идентификатор метаданных")
#     name: str = Field(description="Название файла")
#     location: str = Field(description="Расположение файла в иерархии")
#     file_id: UUID = Field(description="Уникальный идентификатор файла")
#     order_id: UUID = Field(description="Уникальный идентификатор заказа")
#     status: FileStatus = Field(description="Статус файла")
#     index: IndexDTO = Field(description="Индекс связанный с файлом")
#
#
# class OrderDTO(BaseModel, TimesFieldMixin):
#     id: UUID = Field(description="Уникальный идентификатор заказа")
#     files: list[MetaFileDTO] = Field(description="Список файлов, связанных с заказом")
