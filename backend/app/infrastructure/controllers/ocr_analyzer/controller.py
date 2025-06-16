from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.infrastructure.controllers.ocr_analyzer.depends import (
    get_ocr_text_analyzer_service,
)
from app.infrastructure.services.ocr_analyzer import OCRTextAnalyzerService


router = APIRouter(prefix="/pdf", tags=["PDFS"])


@router.post("/analyse/", status_code=200)
async def get_pdf_analyse(
    file: UploadFile = File(...),
    ocr_text_analyzer_service: OCRTextAnalyzerService = Depends(
        get_ocr_text_analyzer_service
    ),
    session: AsyncSession = Depends(get_session),
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Неверный формат файла"
        )

    return await ocr_text_analyzer_service.analysis_pdf_file(file=file, session=session)
