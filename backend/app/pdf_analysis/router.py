from typing import Literal
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.pdf_analysis.service import StatementService
from app.pdf_analysis.models import StatementDTO

router = APIRouter(prefix="/pdf", tags=["PDFS"])


@router.get("/all", status_code=status.HTTP_200_OK,)
async def get_all_analysises(session: AsyncSession = Depends(get_session)
):
    return await StatementService.get_all_analysises(session=session)


@router.post("/analyse/", status_code=200)
async def get_pdf_analyse(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session),
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Неверный формат файла")
    
    return await StatementService.analysis_pdf_file(file, session)

@router.get("/{id}")
async def get_document_by_id(id: int, session: AsyncSession = Depends(get_session)):
    return await StatementService.get_analyse_by_id(id=id, session=session)

@router.delete("/delete/{id}")
async def delete_document_by_id(id: int, session: AsyncSession = Depends(get_session)):
    return await StatementService.delete_analyse_by_id(id=id, session=session)


@router.get("/download/{id}")
async def download_document_by_id(id: int, type: Literal["json", "excel"] = "json", session: AsyncSession = Depends(get_session)):
    return await StatementService.download_analyse_by_id(id=id, type=type, session=session)
