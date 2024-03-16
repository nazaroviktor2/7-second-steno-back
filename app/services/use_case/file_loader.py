from tempfile import NamedTemporaryFile

from loguru import logger

from app.core.minio import minio_loader
from app.ml.whisper import whisper_model_pipeline, convert_whisper_result_to_text


async def file_get_text(order_id: str) -> None:
    """Читает файл и сохраняет его в индекс."""

    with NamedTemporaryFile(delete=True, suffix=".mp4") as tempt_file:
        minio_loader.load_file(save_path=tempt_file.name, file_path=f"0d77b5c5-e0f0-458e-a88f-4080f5dc2772/Женя TextSumm (1).mp4")
        whisper_result = whisper_model_pipeline(tempt_file.name, file_format='mp4')
        text_result = convert_whisper_result_to_text(whisper_result)
    logger.info(text_result)
    # await file.add_to_index(text)
    # await file_metadata_set_status(file.meta_id, FileStatus.SUCCESS)

