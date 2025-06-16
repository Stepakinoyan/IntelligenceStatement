import json
import tempfile
from typing import TypeVar

import openpyxl
from app.domain.repositories.statement import StatementRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.exceptions import AnalyseIsNotFoundException

T = TypeVar("T")


class FileExportService:
    def __init__(self, repository: StatementRepository):
        self._repository = repository

    async def export_to_json(
        cls, id: int, session: AsyncSession
    ) -> tuple[str, str, str]:
        statement = await cls._repository.get(id=id, session=session)
        if not statement:
            raise AnalyseIsNotFoundException

        with tempfile.NamedTemporaryFile(
            "w", suffix=".json", delete=False, encoding="utf-8"
        ) as temp_file:
            json.dump(statement.data, temp_file, ensure_ascii=False, indent=4)
            temp_file_path = temp_file.name

        return (
            temp_file_path,
            "application/json",
            f"{statement.create_at}_{statement.id}.json",
        )

    async def export_to_excel(
        cls, id: int, session: AsyncSession
    ) -> tuple[str, str, str]:
        statement = await cls._repository.get(id=id, session=session)

        if not statement:
            raise AnalyseIsNotFoundException
        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as temp_file:
            temp_file_path = temp_file.name

        wb = openpyxl.Workbook()
        ws = wb.active

        headers = list(statement.data.keys())
        ws.append(headers)

        row_data = [
            ", ".join(v) if isinstance(v, list) else str(v) if v is not None else ""
            for v in statement.data.values()
        ]
        ws.append(row_data)

        wb.save(temp_file_path)

        return (
            temp_file_path,
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            f"{statement.create_at}_{statement.id}.xlsx",
        )
