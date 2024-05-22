from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class UserIn(BaseModel):
    first_name: str
    last_name: Optional[str]

    class Config:
        from_attributes = True


class UserOut(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
