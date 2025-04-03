from fastapi import APIRouter, Depends, UploadFile, File, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.pdf_analysis.service import StatementService
from app.pdf_analysis.models import StatementDTO

router = APIRouter(prefix="/pdf", tags=["PDFS"])


@router.post("/analyse/", status_code=status.HTTP_200_OK)
async def get_pdf_analyse(
    file: UploadFile = File(...), session: AsyncSession = Depends(get_session)
):
    return await StatementService.analysis_pdf_file(file, session)


@router.get("/{id}", response_model=StatementDTO)
async def get_analyse_by_id(id: int, session: AsyncSession = Depends(get_session)):
    return await StatementService.get_analyse_by_id(id=id, session=session)

@router.delete("/delete/{id}")
async def delete_analyse_by_id(id: int, session: AsyncSession = Depends(get_session)):
    return await StatementService.delete_analyse_by_id(id=id, session=session)


@router.get("/download/{id}")
async def download_analyse_by_id(id: int, session: AsyncSession = Depends(get_session)):
    return await StatementService.download_analyse_by_id(id=id, session=session)
