from app.infrastructure.repositories.statement import StatementRepositoryImpl
from sqlalchemy.ext.asyncio import AsyncSession
from app.exceptions import AnalyseIsNotFoundException, SomethingWentWrongException


class StatementService:
    def __init__(cls, repository: StatementRepositoryImpl):
        cls._repository = repository

    async def get_all_analysises(cls, session: AsyncSession):
        return await cls._repository.get_all(session=session)

    async def get_analyse_by_id(cls, id: int, session: AsyncSession):
        item = await cls._repository.get(id=id, session=session)

        if not item:
            raise AnalyseIsNotFoundException

        return item

    async def delete_analyse_by_id(cls, id: int, session: AsyncSession):
        try:
            await cls._repository.delete(id=id, session=session)
        except Exception:
            raise SomethingWentWrongException
