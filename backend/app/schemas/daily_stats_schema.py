from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.constants.enums.week_day import WeekDay


class DailyStatsBase(BaseModel):
    date: datetime
    articles_upload: int
    day_of_week: WeekDay


class DailyStatsCreate(DailyStatsBase):
    pass


class DailyStatsUpdate(DailyStatsBase):
    pass


class DailyStats(DailyStatsBase):
    uid: int
    model_config = ConfigDict(from_attributes=True)
