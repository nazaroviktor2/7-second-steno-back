import os
from abc import ABC, abstractmethod
from tempfile import NamedTemporaryFile, TemporaryDirectory
from uuid import UUID

from loguru import logger

from app.core.config import config
from app.core.fast_stream import atom_search_in, get_publisher
from app.gateways.file_storage.minio import minio_gateway
from app.worker.tasks import (
    file_read_task,
    file_send_to_ocr_task,
    order_set_status_error_task,
    unpack_zip_task,
)
from app.gateways.tika import tika_client
from app.db.db_crud import create_new_file_metadata, file_metadata_set_status
from app.db.models import FileStatus
from app.services.file import MetaFile, ZipFile
from app.schemas.ocr_schemas import OCRRequest

ZIP_TYPE = (
    "application/zip",
    "application/x-zip-compressed",
    "application/vnd.rar",
    "application/x-rar",
)
OCR_TYPE = ("image/jpeg", "image/png")


class BaseProcessing(ABC):
    @abstractmethod
    def processing(self, file: MetaFile) -> None:
        """Запускает обработку файла.

        Parameters
        ----------
        file : MetaFile
            Объект файла, который необходимо обработать
        """


class FileProcessing(BaseProcessing):
    def processing(self, file: MetaFile) -> None:
        """Запускает задачи обработки файла.

        Сериализует данные файла и создает группу задач для их параллельного выполнения.

        Parameters
        ----------
        file : MetaFile
            Объект файла, который необходимо обработать.
        """

        file_data = file.serialize()

        save_task = file_read_task.si(file_data)

        #  задача завершения заказа с ошибкой
        save_task.link_error(order_set_status_error_task.si(str(file.order_id), str(file.meta_id)))

        save_task.apply_async()


class ZipProcessing(BaseProcessing):
    def processing(self, file: MetaFile) -> None:
        """Запускает задачи обработки архива,

        Сериализует данные файла и создает группу задач для их параллельного выполнения.

        Parameters
        ----------
        file : MetaFile
            Объект файла, который необходимо обработать.

        """

        file_data = file.serialize()

        # Группа задач для последовательно выполнения
        save_and_unpack = unpack_zip_task.si(file_data)

        #  задача завершения заказа с ошибкой
        save_and_unpack.link_error(order_set_status_error_task.si(str(file.order_id), str(file.meta_id)))

        save_and_unpack.apply_async()


class OCRProcessing(BaseProcessing):
    def processing(self, file: MetaFile) -> None:
        """Запускает задачи обработки фотографий"""

        file_data = file.serialize()

        send_to_ocr = file_send_to_ocr_task.si(file_data)

        #  задача завершения заказа с ошибкой
        send_to_ocr.link_error(order_set_status_error_task.si(str(file.order_id), str(file.meta_id)))

        send_to_ocr.apply_async()


def get_strategy_from_type(file_type: str) -> BaseProcessing:
    """Возвращает стратегию обработки файла в зависимости от его типа."""
    if file_type in OCR_TYPE:
        return OCRProcessing()
    elif file_type in ZIP_TYPE:
        return ZipProcessing()
    else:
        return FileProcessing()


def start_processing(file: MetaFile) -> None:
    """Запускает обработку файла из ходя из типа."""
    get_strategy_from_type(file.type).processing(file)


async def file_set_status_error(serialized_file: str) -> None:
    """Завершает файл со статусом ошибки."""
    file = MetaFile.deserialize(serialized_file)
    await file_metadata_set_status(file.meta_id, FileStatus.UPLOAD_ERROR)
    logger.info(f"Файл с id = '{file.meta_id}' - завершился с ошибкой")


async def order_set_status_error(order_id: UUID, meta_id: UUID) -> None:
    """Завершает файл со статусом ошибки."""
    await file_metadata_set_status(meta_id, FileStatus.ERROR)
    logger.info(f"Заказ с id = '{order_id}' - завершился с ошибкой")


async def file_read(serialized_file: str) -> None:
    """Читает файл и сохраняет его в индекс."""
    file = MetaFile.deserialize(serialized_file)
    with NamedTemporaryFile(delete=False, suffix=file.filename) as tempt_file:
        minio_gateway.load_file(file_storage_path=tempt_file.name, file_path=file.path)
        text = await tika_client.get_text(tempt_file.name)
    await file.add_to_index(text)
    await file_metadata_set_status(file.meta_id, FileStatus.SUCCESS)


async def send_file_to_ocr(serialized_file: str) -> None:
    """Отправляет файл на чтение в ocr"""
    file = MetaFile.deserialize(serialized_file)
    async with get_publisher() as publisher:
        await publisher.publish(
            OCRRequest(
                guid=str(file.meta_id),
                minio_path=file.path,
                bucket=config.MINIO_BUCKET,
            ),
            atom_search_in,
        )


async def unpack_zip(serialized_file: str) -> None:
    """Распаковывает архив."""
    file = ZipFile.deserialize(serialized_file)
    logger.info(
        f"Началась распаковки архива '{file.filename}' из заказа '{file.order_id}'",
    )
    await file_metadata_set_status(file.meta_id, FileStatus.UNPACKING)

    with TemporaryDirectory() as folder:
        file.unpack(folder)
        await process_folder(file, folder, file.location)

    # ставим архиву статут обработан, так как не будет читать текст из него
    await file_metadata_set_status(file.meta_id, FileStatus.SUCCESS)


async def process_folder(file: MetaFile, path: str, location: str) -> None:
    """Обрабатывает содержимое папки, создавая и обрабатывая файлы.

    Parameters
    ----------
    file : MetaFile
        Экземпляр LocalFile, представляющий родительский файл
    path : str
        Путь к обрабатываемой папке
    location : str
        Расположение в иерархии файлов
    """
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        try:
            if os.path.isfile(item_path):
                await process_file(file, item_path, location)
            elif os.path.isdir(item_path):
                await process_folder(file, item_path, location + "/" + item)
        except Exception as error:
            logger.exception(f"Ошибка при обработке файла или папки: {error}")


async def process_file(file: MetaFile, item_path: str, location: str) -> None:
    """Обрабатывает отдельный файл в папке.

    Для каждого подходящего файла запускаются задачи обработки.

    Parameters
    ----------
    file : MetaFile
        Экземпляр `MetaFile`, представляющий родительский файл
    item_path : str
        Путь к обрабатываемому файлу
    location : str
        Расположение в иерархии файлов
    """

    new_file, correct = await MetaFile.create_from_path(
        order_id=file.order_id,
        index_id=file.index_id,
        file_path=item_path,
        location=location,
        parent_id=file.meta_id,
    )

    if correct:
        start_processing(new_file)
    else:
        # нельзя сохранять хеш не верных файлов, так как если мы в будущем добавим их подержу
        # новые заказы с этими же файлами будут ссылаться
        # на прошлую запись с таким же хешом и со статусом UNSUPPORTED

        await create_new_file_metadata(
            file_id=new_file.file_id,
            order_id=new_file.order_id,
            index_id=file.index_id,
            location=new_file.location,
            name=new_file.filename,
            parent_id=file.parent_id,
            status=FileStatus.UNSUPPORTED_TYPE,
        )
