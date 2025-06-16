from datetime import datetime

from sqlmodel import SQLModel


class StatementDTO(SQLModel):
    create_at: datetime
    data: dict[str, str | list[str]]
