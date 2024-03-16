
from celery import Task
from loguru import logger

from app.core.celery import app_celery
from app.core.helpers import run_task_in_event_loop
from app.services.exceptions import DomainError


@app_celery.task(bind=True)
def file_read_task(self: Task, serialized_file: str) -> None:
    """Задача чтения файла"""
    from app.services.use_case.file_loader import file_read

    try:
        run_task_in_event_loop(file_read(serialized_file))
    except DomainError as error:
        logger.error(f"Error with task {self.request.id}: {error}")
        raise

