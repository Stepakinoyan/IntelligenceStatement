from sqlalchemy import insert
from app.pdf_analysis.models import Statement
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError


class StatementsDAO:
    model = Statement

    @classmethod
    async def add(cls, session: AsyncSession, **data):
        try:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()
        except SQLAlchemyError:
            await session.rollback()
