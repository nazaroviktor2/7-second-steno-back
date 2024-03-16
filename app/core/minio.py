import io

from loguru import logger
from minio import Minio, S3Error

from app.core.config import config


class MinioLoader:
    def __init__(self, minio_bucket: str):
        self.client = Minio(
            config.MINIO_ENDPOINT,
            access_key=config.MINIO_LOGIN,
            secret_key=config.MINIO_PASS,
            secure=False,
        )
        self.minio_bucket = minio_bucket

    def save_file_from_path(
        self,
        minio_path: str,
        file_path: str,
        minio_bucket: str | None = None,
    ) -> None:
        """Сохраняет файл с диска в minio."""
        # Если минио_бакет не задан, используем тот, который по умолчанию
        if not minio_bucket:
            minio_bucket = self.minio_bucket

        logger.info(f"Сохраняем в Minio dir '{minio_path}' файл '{file_path}' ")
        try:
            if not self.client.bucket_exists(minio_bucket):
                self.client.make_bucket(minio_bucket)

            self.client.fput_object(minio_bucket, minio_path, file_path)

            logger.info(f"`{file_path}` сохранен в minio")
        except S3Error:
            logger.error("#" * 20)
            logger.exception("Error with minion save_file")

    def save_file_from_bytes(
        self,
        minio_path: str,
        file_bytes: bytes,
        file_size: int,
        minio_bucket: str | None = None,
    ) -> None:
        """Сохраняет файл из байтов в minio."""
        # Если минио_бакет не задан, используем тот, который по умолчанию
        if not minio_bucket:
            minio_bucket = self.minio_bucket

        logger.info(f"Сохраняем в Minio dir '{minio_path}'")
        try:
            if not self.client.bucket_exists(minio_bucket):
                self.client.make_bucket(minio_bucket)

            self.client.put_object(minio_bucket, minio_path, io.BytesIO(file_bytes), file_size)

        except S3Error:
            logger.error("#" * 20)
            logger.exception("Error with minion save_file")

    def load_file(
        self,
        file_path: str,
        save_path: str,
        minio_bucket: str | None = None,
    ) -> str:
        """Загружает файл из хранилища Minio и сохраняет его локально."""
        # Если минио_бакет не задан, используем тот, который по умолчанию
        if not minio_bucket:
            minio_bucket = self.minio_bucket

        logger.info(f"Загружаем из Minio {file_path}")
        try:
            self.client.fget_object(minio_bucket, file_path, save_path)

        except S3Error:
            logger.error("#" * 20)
            logger.exception("Error with minion load_file")

        else:
            logger.info(f"Успешно загружено {file_path}")
            return save_path


minio_loader = MinioLoader(minio_bucket=config.MINIO_BUCKET)
