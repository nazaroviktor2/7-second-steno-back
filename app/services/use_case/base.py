import abc
import dataclasses
from typing import Generic, TypeVar


@dataclasses.dataclass(frozen=True)
class UCPayload(abc.ABC):
    """Базовый класс параметров."""


@dataclasses.dataclass(frozen=True)
class UCResult(abc.ABC):
    """Базовый класс результата."""


_PayloadT = TypeVar("_PayloadT", bound=UCPayload)
_ResultT = TypeVar("_ResultT", bound=UCResult)


class UseCase(abc.ABC, Generic[_PayloadT]):
    """Базовый класс сценария без результата."""

    @abc.abstractmethod
    async def execute(self, payload: _PayloadT) -> None:
        """Запуск сценария."""


class UseCaseResulted(abc.ABC, Generic[_PayloadT, _ResultT]):
    """Базовый класс сценария возвращающий результат."""

    @abc.abstractmethod
    async def execute(self, payload: _PayloadT) -> _ResultT:
        """Запуск сценария с результатом."""
