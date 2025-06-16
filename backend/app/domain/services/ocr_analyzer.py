from abc import ABC, abstractmethod
from typing import TypeAlias

from app.domain.repositories.statement import StatementRepository

JSON: TypeAlias = dict[str, "JSON"] | list["JSON"] | str | int | float | bool | None


class OCRTextAnalyzerAbctractService(ABC):
    def __init__(self, repository: StatementRepository):
        self._repository = repository

    @abstractmethod
    def extract_text(pdf_bytes: bytes) -> str: ...

    @abstractmethod
    async def analyze_text(text: str) -> JSON: ...
