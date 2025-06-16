from fastapi import FastAPI
from app.infrastructure.controllers.statement.controller import (
    router as statements_router,
)
from app.infrastructure.controllers.ocr_analyzer.controller import (
    router as ocr_analyzer_router,
)
from app.infrastructure.controllers.file_export.controller import (
    router as file_export_router,
)
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(statements_router)
app.include_router(ocr_analyzer_router)
app.include_router(file_export_router)
