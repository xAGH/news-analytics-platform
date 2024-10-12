from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.config.database_config import Base


class NewcastModel(Base):
    __tablename__ = "newcast"

    uid = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True, nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.now())
    articles = relationship("ArticleModel", back_populates="newcast")
    stats = relationship("StatsModel", back_populates="newcast")
