import json
import tempfile
from fastapi import HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from app.pdf_analysis.utils import extract_text_with_ocr, analysis_pdf_files
from sqlalchemy.ext.asyncio import AsyncSession
from app.pdf_analysis.dao import StatementsDAO
from app.pdf_analysis.exceptions import SomethingWentWrongException, AnalyseIsNotFoundException


class StatementService:
    @classmethod
    async def analysis_pdf_file(cls, file: UploadFile, session: AsyncSession):
        try:
            file_bytes = await file.read()

            text = extract_text_with_ocr(pdf_bytes=file_bytes)

            analyse = await analysis_pdf_files(text)
            await StatementsDAO.add(analyse=analyse, session=session)

            return analyse
        except Exception:
            raise SomethingWentWrongException

    @classmethod
    async def get_analyse_by_id(cls, id: int, session: AsyncSession):
        item = await StatementsDAO.get_analyse_by_id(id=id, session=session)

        if not item:
            raise HTTPException(
                detail="Analyse is not found.", status_code=status.HTTP_404_NOT_FOUND
            )

        return item

    @classmethod
    async def delete_analyse_by_id(cls, id: int, session: AsyncSession):
        try:
            await StatementsDAO.delete_analyse_by_id(id=id, session=session)

        except Exception:
            raise SomethingWentWrongException
        
    @classmethod
    async def download_analyse_by_id(cls, id: int, session: AsyncSession):
        statement = await StatementsDAO.get_analyse_by_id(id=id, session=session)
        if not statement:
            raise AnalyseIsNotFoundException
        
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as temp_file:
            json.dump(statement.data, temp_file, ensure_ascii=False, indent=4)
            temp_file_path = temp_file.name
        
        return FileResponse(temp_file_path, media_type="application/json", filename=f"{statement.create_at}_{statement.id}.json")