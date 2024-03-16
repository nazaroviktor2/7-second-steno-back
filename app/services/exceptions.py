from collections.abc import Callable
from functools import wraps
from typing import Any
from uuid import UUID

from fastapi import HTTPException, status

from app.core.config import config

NOT_AVAILABLE_FILE_TYPE = "File type '{file_type}' is not available"
HASH_ALREADY_EXISTS = "File with hash '{file_hash}' already exists"
TOO_MUCH_SIZE = "The file with {size} is too large. Max size is {max_size} bytes"
ORDER_NOT_FOUND = "Order with id = '{id}' not found"
FILE_NOT_FOUND = "File with id = '{id}' not found"
INDEX_NOT_FOUND_BY_NAME = "Index with name = '{name}' not found"
INDEX_NOT_FOUND_BY_ID = "Index with id = '{id}' not found"
NOT_FOUND = "Not found"


def handle_domain_error(func: Callable) -> Any:
    """Декоратор для обработки `DomainError`."""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except DomainError as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(error),
            )

    return wrapper


class DomainError(Exception):
    """Доменные исключения."""


class FileSizeError(DomainError):
    """FileSize exception class."""

    def __init__(self, size: int):
        super().__init__(TOO_MUCH_SIZE.format(size=size, max_size=config.MAX_SIZE))


class FileTypeError(DomainError):
    """FileType exception class."""

    def __init__(self, file_type: str):
        super().__init__(NOT_AVAILABLE_FILE_TYPE.format(file_type=file_type))


class OrderNotFoundError(DomainError):
    """OrderNotFoundError exception class."""

    def __init__(self, order_id: str | UUID):
        super().__init__(ORDER_NOT_FOUND.format(id=order_id))


class UploadFileNotFoundError(DomainError):
    """UploadFileNotFoundError exception class."""

    def __init__(self, file_id: str | UUID):
        super().__init__(FILE_NOT_FOUND.format(id=file_id))


class MetaFileNotFoundError(UploadFileNotFoundError):
    pass


class IndexNotFoundError(DomainError):
    """IndexNotFoundError exception class."""

    def __init__(self, index_name: str | None = None, index_id: UUID | None = None):
        if index_name:
            super().__init__(INDEX_NOT_FOUND_BY_NAME.format(name=index_name))

        elif index_id:
            super().__init__(INDEX_NOT_FOUND_BY_ID.format(id=index_id))

        else:
            super().__init__(NOT_FOUND)
