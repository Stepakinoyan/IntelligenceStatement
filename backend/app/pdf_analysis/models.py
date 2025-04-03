from sqlmodel import JSON, Column, SQLModel, Field
from sqlalchemy import DateTime
from datetime import datetime
from pytz import timezone


class Statement(SQLModel, table=True):
    id: int = Field(primary_key=True)
    create_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone("Asia/Yakutsk")),
        sa_column=Column(DateTime(timezone=True)),
    )
    data: dict[str, str] = Field(sa_column=Column(JSON))
