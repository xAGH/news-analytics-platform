from pydantic import BaseModel


class Populate(BaseModel):
    newcast_uid: int
    months_to_populate: int
    min_articles_per_day: int
    max_articles_per_day: int
