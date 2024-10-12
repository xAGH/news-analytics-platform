from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ArticleBase(BaseModel):
    upload_date: datetime
    file_path: str
    newcast_uid: int


class Article(ArticleBase):
    uid: int
    model_config = ConfigDict(from_attributes=True)
