from sqlalchemy import insert, select
from app.pdf_analysis.models import Statement
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError


class StatementsDAO:
    model = Statement

    @classmethod
    async def add(cls, session: AsyncSession, analyse: dict):
        try:
            query = insert(cls.model).values(data=analyse)
            await session.execute(query)
            await session.commit()
        except SQLAlchemyError:
            await session.rollback()

    @classmethod
    async def get_analyse_by_id(cls, id: int, session: AsyncSession):
        item = select(cls.model).filter_by(id=id)
        result = await session.execute(item)

        return result.scalar_one_or_none()
