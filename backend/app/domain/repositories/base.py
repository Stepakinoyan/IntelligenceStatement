from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class BaseAbstractRepository(ABC, Generic[T]):
    def __init__(self, model: T):
        self.model = model

    @abstractmethod
    async def add(cls, **entity) -> T:
        pass

    @abstractmethod
    async def get(cls, id: int) -> T | None:
        pass

    @abstractmethod
    async def delete(cls, id: int) -> None:
        pass

    @abstractmethod
    async def get_all(cls) -> list[T]:
        pass
