from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from app.schemas.article_schema import Article


class NewcastBase(BaseModel):
    name: str


class NewcastCreate(NewcastBase):
    pass


class NewcastUpdate(NewcastBase):
    pass


class Newcast(NewcastBase):
    uid: int
    created_at: datetime
    articles: Optional[List[Article]] = []
    model_config = ConfigDict(from_attributes=True)
