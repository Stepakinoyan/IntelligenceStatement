from app.infrastructure.entities.statement import Statement
from app.infrastructure.repositories.statement import StatementRepositoryImpl
from app.infrastructure.services.ocr_analyzer import OCRTextAnalyzerService


def get_ocr_text_analyzer_service() -> OCRTextAnalyzerService:
    repo = StatementRepositoryImpl(model=Statement)

    return OCRTextAnalyzerService(repository=repo)
