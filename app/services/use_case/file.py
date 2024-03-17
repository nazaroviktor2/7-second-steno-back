import uuid
from uuid import UUID

from loguru import logger

# from app.db.db_crud import (
#     create_new_order,
#     get_file_metadata_by_id,
# )
# from app.db.models import FileMetadata

from app.core.minio import minio_loader
from app.db.db_crud import create_new_order, order_add_minio_path
from app.schemas.file_schemas import UploadFileIn
from app.worker.tasks import file_get_text_task
# from app.services.use_case.file_loader import start_processing

PATH = "{order_id}/{filename}"


async def service_file_upload(payload: UploadFileIn, priority: bool = False) -> str:
    """Обрабатывает загрузку файла и создает новый заказ."""
    logger.info(f"get a file to upload {payload}")
    order_id = await create_new_order(payload.name)
    order_id = str(order_id)
    path = PATH.format(order_id=order_id, filename=payload.file.filename)
    minio_loader.save_file_from_bytes(path, payload.file.file.read(), payload.file.size)
    await order_add_minio_path(order_id, path)
    save_task = file_get_text_task.si(order_id, path)
    save_task.apply_async()

    return order_id


# async def service_get_file(file_id: UUID) -> FileMetadata:
#     """Возвращает файл."""
#     return await get_file_metadata_by_id(file_id)
