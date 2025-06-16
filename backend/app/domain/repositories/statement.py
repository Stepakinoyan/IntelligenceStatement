from abc import ABC
from app.domain.entities.statement import Statement
from app.domain.repositories.base import BaseAbstractRepository


class StatementRepository(BaseAbstractRepository[Statement], ABC): ...
