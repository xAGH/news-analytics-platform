from sqlalchemy import Column, Date, Enum, Integer
from sqlalchemy.orm import relationship

from app.config.database_config import Base
from app.constants.enums.week_day import WeekDay


class DailyStatsModel(Base):
    __tablename__ = "daily_stats"

    uid = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date = Column(Date, nullable=False)
    articles_upload = Column(Integer, nullable=False)
    day_of_week = Column(Enum(WeekDay), nullable=False)
