import enum
import uuid

from sqlalchemy import (
    UUID,
    Column,
    DateTime,
    String,
    func, Enum,
)
from sqlalchemy.orm import mapped_column

from app.db.database import Base


class OrderStatus(enum.Enum):
    in_queue: str = "В очереди"
    in_process: str = "В работе"
    done: str = "Завершен"


class TimesFieldsMixin:
    """Mixin добавляющий таблице БД поля created_at и updated_at"""
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now())


class Order(Base, TimesFieldsMixin):
    __tablename__ = "order"

    id = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )
    name = Column(String)
    status = Column(Enum(OrderStatus), default=OrderStatus.in_queue, nullable=False)
    preview = Column(String, default="")
    minio_path = Column(String, default="")
