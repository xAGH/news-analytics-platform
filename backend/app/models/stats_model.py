from sqlalchemy import Column, Date, Enum, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.config.database_config import Base
from app.constants.enums.week_day import WeekDay


class StatsModel(Base):
    __tablename__ = "stats"

    uid = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date = Column(Date, nullable=False)
    articles_upload = Column(Integer, nullable=False)
    day_of_week = Column(Enum(WeekDay), nullable=False)
    newcast_uid = Column(Integer, ForeignKey("newcast.uid"), nullable=False)
    newcast = relationship("NewcastModel", back_populates="stats")
