import json
from fastapi import UploadFile
from httpx import AsyncClient
from pdf2image import convert_from_bytes
import pytesseract
from app.core.config import settings
from app.exceptions import SomethingWentWrongException
from app.domain.services.ocr_analyzer import JSON, OCRTextAnalyzerAbctractService
from sqlalchemy.ext.asyncio import AsyncSession


class OCRTextAnalyzerService(OCRTextAnalyzerAbctractService):
    def extract_text(self, pdf_bytes: bytes) -> str:
        images = convert_from_bytes(pdf_bytes)
        text = "\n".join(
            [pytesseract.image_to_string(image, lang="rus") for image in images]
        )
        return text

    async def analyze_text(self, text: str) -> JSON:
        async with AsyncClient(timeout=300) as client:
            url = f"https://api.cloudflare.com/client/v4/accounts/{settings.ACCOUNT_ID}/ai/run/{settings.MODEL}"
            headers = {
                "Authorization": f"Bearer {settings.API_TOKEN}",
                "Content-Type": "application/json",
            }
            data = {
                "messages": [
                    {
                        "role": "system",
                        "content": "Ты ассистент юриста, тебе дают текст судебного завяления, вноси исправление ошибок в текст как орфографических, так и в соответсвии с законодательством Российской Федерации. Сам текст отсканирован через OCR следовательно в нём есть артефакты, если сможешь, попробуй их поправить, если не сможет, то не учитывай их.",
                    },
                    {
                        "role": "user",
                        "content": f"Проанализируй текст '{text}', отформатируй вывод параметров по принципу ключ значение, выводи строго в формате JSON, НЕ ПИШИ НИЧЕГО ДРУГОГО КРОМЕ ГОТОВОГО JSON, УМОЛЯЮ, я тебе даю задачу, проанализируй текст и постарайся логически найти упоминание следующих элементов: Наименование суда, Взыскатель, Юридический адрес взыскателя. Телефон взыскателя. ИНН взыскателя,"
                        "Адрес взыскателя для корреспонденции, Должник,"
                        "Адрес должника, Дата рождения должника, Место"
                        "рождения лица, Паспорт серия должника, Паспорт"
                        "номер должника, Паспорт дата выдачи должника,"
                        "Паспорт орган выдавший паспорт должника, ИНН"
                        "должника, СНИЛС должника, Сущность взыскания,"
                        "Адрес взыскания, Пропорциональный порядок"
                        "взыскания, Доли взыскания, Солидарный порядок"
                        "взыскания, Наименование услуги, Долг, Сумма долга,"
                        "Начало периода долга, Конец периода долга, Пеня,"
                        "Сумма пени, Начало периода пени, Конец периода"
                        "пени, Процент, Сумма по процентам, Начало периода"
                        "по процентам, Конец периода по процентам, Штраф,"
                        "Сумма штрафа, Начало периода штрафа, Конец"
                        "периода штрафа, Иное взыскание Сумма иного"
                        "взыскания, Начало периода иного взыскания, Конец"
                        "периода иного взыскания, Общая сумма взыскания,"
                        "Госпошлина, Приложение к заявлению. ЕСЛИ ТЫ НЕ НАШЕЛ ЗНАЧЕНИЕ, ТО ПРОСТО НЕ ПИШИ В ЗНАЧЕНИИ КЛЮЧА, ОСТАВЬ САМ КЛЮЧ. В элементе 'Приложение к заявлению' выводи в виде списка эти самые приложения к заявлению, ЕСЛИ ИХ ТЫ НЕ НАШЕЛ, ТО ЛИСТ ПУСТОЙ.",
                    },
                ],
                "max_tokens": 4000,
            }

            response = await client.post(url, headers=headers, json=data)
            data = json.loads(
                response.json()["result"]["response"].strip("```").lstrip("json")
            )

            return data

    async def analysis_pdf_file(cls, file: UploadFile, session: AsyncSession):
        try:
            file_bytes = await file.read()

            text = cls.extract_text(pdf_bytes=file_bytes)

            analyse = await cls.analyze_text(text)
            await cls._repository.add(data=analyse, session=session)

            return analyse
        except Exception:
            raise SomethingWentWrongException
