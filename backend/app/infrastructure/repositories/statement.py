from app.domain.repositories.statement import StatementRepository
from sqlalchemy import delete, select, insert
from sqlalchemy.ext.asyncio import AsyncSession


class StatementRepositoryImpl(StatementRepository):
    async def add(cls, session: AsyncSession, **entity):
        query = insert(cls.model).values(**entity)
        await session.execute(query)
        await session.commit()

    async def get(cls, id: int, session: AsyncSession):
        query = select(cls.model).filter_by(id=id)
        query = await session.execute(query)

        return query.scalars().first()

    async def delete(cls, id: int, session: AsyncSession) -> None:
        query = delete(cls.model).filter_by(id=id)
        await session.execute(query)

        await session.commit(query)

    async def get_all(cls, session: AsyncSession):
        items = select(cls.model.create_at, cls.model.id)
        items = await session.execute(items)

        return items.mappings().all()
