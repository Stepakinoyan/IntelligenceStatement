from sqlmodel import JSON, Column, SQLModel, Field
from sqlalchemy import DateTime
from pytz import timezone
from datetime import datetime


class Statement(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    create_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            default=lambda: datetime.now(timezone("Asia/Yakutsk")),
            nullable=False,
        )
    )
    data: dict[str, str] = Field(sa_column=Column(JSON))
