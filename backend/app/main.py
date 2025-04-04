from fastapi import FastAPI
from app.pdf_analysis.router import router as pdfs_router
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

app.include_router(pdfs_router)
