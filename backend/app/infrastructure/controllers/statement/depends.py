from app.infrastructure.entities.statement import Statement
from app.infrastructure.repositories.statement import StatementRepositoryImpl
from app.infrastructure.services.statement import StatementService


def get_statement_service() -> StatementService:
    repo = StatementRepositoryImpl(model=Statement)
    return StatementService(repository=repo)
