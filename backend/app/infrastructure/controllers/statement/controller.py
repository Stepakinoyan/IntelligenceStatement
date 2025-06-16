from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.infrastructure.controllers.statement.depends import get_statement_service
from app.infrastructure.services.statement import StatementService

router = APIRouter(prefix="/statements", tags=["Statements"])


@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
)
async def get_all_analysises(
    statement_service: StatementService = Depends(get_statement_service),
    session: AsyncSession = Depends(get_session),
):
    return await statement_service.get_all_analysises(session=session)


@router.get("/document/{id}")
async def get_document_by_id(
    id: int,
    statement_service: StatementService = Depends(get_statement_service),
    session: AsyncSession = Depends(get_session),
):
    return await statement_service.get_analyse_by_id(id=id, session=session)


@router.delete("/delete/{id}")
async def delete_document_by_id(
    id: int,
    statement_service: StatementService = Depends(get_statement_service),
    session: AsyncSession = Depends(get_session),
):
    return await statement_service.delete_analyse_by_id(id=id, session=session)
