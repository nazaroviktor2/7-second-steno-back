import uuid
from uuid import UUID

from loguru import logger

# from app.db.db_crud import (
#     create_new_order,
#     get_file_metadata_by_id,
# )
# from app.db.models import FileMetadata

from app.core.minio import minio_loader
from app.schemas.file_schemas import UploadFileIn
# from app.services.use_case.file_loader import start_processing

PATH = "{order_id}/{filename}"


async def service_file_upload(payload: UploadFileIn) -> str:
    """Обрабатывает загрузку файла и создает новый заказ."""
    logger.info(f"get a file to upload {payload}")

    # order_id = await create_new_order()
    order_id = str(uuid.uuid4())
    path = PATH.format(order_id=order_id, filename=payload.file.filename)
    minio_loader.save_file_from_bytes(path, payload.file.file.read(), payload.file.size)

    save_task = file_read_task.si(file_data)

    # start_processing(file)
    return order_id


# async def service_get_file(file_id: UUID) -> FileMetadata:
#     """Возвращает файл."""
#     return await get_file_metadata_by_id(file_id)
