from uuid import UUID

from loguru import logger

from app.db.db_crud import (
    create_new_order,
    get_file_metadata_by_id,
)
from app.db.models import FileMetadata
from app.services.file import MetaFile
from app.schemas.file_schemas import UploadFileIn
from app.services.use_case.file_loader import start_processing


async def service_file_upload(payload: UploadFileIn) -> UUID:
    """Обрабатывает загрузку файла и создает новый заказ."""
    logger.info(f"get a file to upload {payload}")

    order_id = await create_new_order()

    file = await MetaFile.create_from_upload_file(
        order_id,
        payload.file,
        payload.index,
        payload.location,
    )

    start_processing(file)
    return order_id


async def service_get_file(file_id: UUID) -> FileMetadata:
    """Возвращает файл."""
    return await get_file_metadata_by_id(file_id)
