from dataclasses import dataclass
from datetime import datetime


@dataclass
class Statement:
    id: int
    create_at: datetime
    data: dict[str, str | list[str]]
