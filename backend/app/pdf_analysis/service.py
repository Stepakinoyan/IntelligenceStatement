import aiofiles
from fastapi import HTTPException, UploadFile, status
from app.pdf_analysis.utils import extract_text_with_ocr, analysis_pdf_files
from sqlalchemy.ext.asyncio import AsyncSession
from app.pdf_analysis.dao import StatementsDAO

class StatementService:
    @classmethod
    async def analysis_pdf_file(self, file: UploadFile, session: AsyncSession):
        # try:
            file_path = f"/mnt/d/Stepa/IntelligenceStatement/backend/app/pdf_analysis/pdfs/{file.filename}"

            async with aiofiles.open(file_path, "wb") as f:
                await f.write(file.file.read())

            text = extract_text_with_ocr(pdf_path=file_path)

            analyse = await analysis_pdf_files(text)
            await StatementsDAO.add(analyse, session=session)

            return analyse
        # except Exception:
        #     raise HTTPException(
        #         detail="Something went wrong...",
        #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        #     )
