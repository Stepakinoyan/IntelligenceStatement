from typing import Literal
from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.domain.services.file_export import FileExportService
from app.infrastructure.controllers.file_export.depends import get_file_export_service

router = APIRouter(prefix="/download", tags=["Download files"])


@router.get("/{id}")
async def download_document_by_id(
    id: int,
    type: Literal["json", "excel"] = "json",
    file_export_service: FileExportService = Depends(get_file_export_service),
    session: AsyncSession = Depends(get_session),
):
    if type == "json":
        temp_file_path, media_type, filename = await file_export_service.export_to_json(
            id=id, session=session
        )
    else:
        (
            temp_file_path,
            media_type,
            filename,
        ) = await file_export_service.export_to_excel(id=id, session=session)

    return FileResponse(path=temp_file_path, media_type=media_type, filename=filename)
