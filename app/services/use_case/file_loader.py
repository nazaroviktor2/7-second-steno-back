from tempfile import NamedTemporaryFile

from loguru import logger

from app.core.celery import search_client
from app.core.minio import minio_loader
from app.db.db_crud import get_order_by_id, order_set_status, order_add_preview
from app.db.models import OrderStatus
from app.ml.summarization import run_summarize_text, summarize_person_text
from app.ml.whisper import whisper_model_pipeline, convert_whisper_result_to_text
from app.services.use_case.index import add_doc_to_index


async def file_get_text(order_id: str, file_path: str) -> None:
    """Читает файл и сохраняет его в индекс."""

    with NamedTemporaryFile(delete=True, suffix=".mp4") as tempt_file:
        minio_loader.load_file(save_path=tempt_file.name, file_path=file_path)
        whisper_result = whisper_model_pipeline(tempt_file.name, file_format='mp4')
        text_result = convert_whisper_result_to_text(whisper_result)

    all_summarize = run_summarize_text(text_result, max_new_tokens=80)
    preview = run_summarize_text(all_summarize, max_new_tokens=20)
    # logger.info(f"PREVIEW ={preview}")
    # logger.info(f"all_summarize ={all_summarize}")
    # logger.info(text_result)
    summary = [
        {'name': "SPEAKER_01", "text": summarize_person_text(text_result, speaker_name='SPEAKER_01')},
        {"name": "All", "text": all_summarize}
    ]
    await order_add_preview(order_id, preview)
    order = await get_order_by_id(order_id)

    add_doc_to_index(
        text=text_result,
        preview=preview,
        summary=summary,
        persons=["Максим", "Кирилл"],
        order_id=order_id,
        name=order.name,
        file_path=file_path
    )

    await order_set_status(order_id, OrderStatus.done)

    # await file.add_to_index(text)
    # await file_metadata_set_status(file.meta_id, FileStatus.SUCCESS)

