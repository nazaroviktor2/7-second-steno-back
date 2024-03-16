import asyncio
import inspect
from collections.abc import Coroutine
from typing import Any

from loguru import logger

from app.core.config import config


def get_or_create_event_loop() -> asyncio.AbstractEventLoop:
    """Возвращает asyncio event loop."""
    try:
        return asyncio.get_event_loop_policy().get_event_loop()
    except RuntimeError:
        loop = asyncio.get_event_loop_policy().new_event_loop()
        asyncio.set_event_loop(loop)
        return loop


def run_task_in_event_loop(coroutine: Coroutine) -> Any:
    """Запускает асинхронную задачу в текущем event loop."""
    if config.TASK_ALWAYS_EAGER:
        asyncio.create_task(coroutine)
        return

    caller = inspect.stack()[1].function

    logger.info(f"{caller}: Started")

    loop = get_or_create_event_loop()

    try:
        result = loop.run_until_complete(coroutine)
    except Exception:
        logger.exception(f"{caller}: Failed")
        raise
    else:
        logger.info(f"{caller}: Finished")
        return result
