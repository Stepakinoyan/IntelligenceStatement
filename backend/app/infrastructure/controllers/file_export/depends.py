from app.infrastructure.entities.statement import Statement
from app.infrastructure.repositories.statement import StatementRepositoryImpl
from app.domain.services.file_export import FileExportService


def get_file_export_service() -> FileExportService:
    repo = StatementRepositoryImpl(model=Statement)
    return FileExportService(repository=repo)
