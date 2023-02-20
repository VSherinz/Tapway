from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class FootagePredicates(BaseModel):
    image_frame: str
    prob: float
    tags: Optional[list[str]]


class FootageData(BaseModel):
    license_id: int
    preds: Optional[list[FootagePredicates]]


class Footage(BaseModel):
    device_id: str
    client_id: int
    created_at: datetime
    data: FootageData



