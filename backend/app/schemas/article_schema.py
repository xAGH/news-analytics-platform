from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ArticleBase(BaseModel):
    upload_date: datetime
    file_path: str
    newspaper_id: int


class ArticleCreate(ArticleBase):
    pass


class ArticleUpdate(ArticleBase):
    pass


class Article(ArticleBase):
    uid: int
    model_config = ConfigDict(from_attributes=True)
