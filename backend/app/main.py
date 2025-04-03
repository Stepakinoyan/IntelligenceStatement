from fastapi import FastAPI
from app.pdf_analysis.router import router as pdfs_router

app = FastAPI()

app.include_router(pdfs_router)
