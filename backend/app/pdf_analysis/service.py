import aiofiles
from fastapi import HTTPException, UploadFile, status
from app.pdf_analysis.utils import extract_text_with_ocr, analysis_pdf_files
from sqlalchemy.ext.asyncio import AsyncSession
from app.pdf_analysis.dao import StatementsDAO


class StatementService:
    @classmethod
    async def analysis_pdf_file(cls, file: UploadFile, session: AsyncSession):
        # try:
            file_bytes = await file.read()

            text = extract_text_with_ocr(pdf_bytes=file_bytes)

            analyse = await analysis_pdf_files(text)
            await StatementsDAO.add(analyse=analyse, session=session)

            return analyse
        # except Exception:
        #     raise HTTPException(
        #         detail="Something went wrong...",
        #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        #     )

    @classmethod
    async def get_analyse_by_id(cls, id: int, session: AsyncSession):
        item = await StatementsDAO.get_analyse_by_id(id=id, session=session)

        if not item:
            raise HTTPException(
                detail="Analyse is not found.", status_code=status.HTTP_404_NOT_FOUND
            )

        return item
