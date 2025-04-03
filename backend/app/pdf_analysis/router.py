from fastapi import APIRouter, Depends, UploadFile, File, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.pdf_analysis.service import StatementService


router = APIRouter(prefix="/pdf", tags=["PDFS"])


@router.post("/analyse/", status_code=status.HTTP_200_OK)
async def get_pdf_analyse(file: UploadFile = File(...), session: AsyncSession = Depends(get_session)):
    return await StatementService.analysis_pdf_file(file, session)
