from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.config.database_config import Base


class ArticleModel(Base):
    __tablename__ = "article"

    uid = Column(Integer, primary_key=True, index=True, autoincrement=True)
    upload_date = Column(DateTime, nullable=False)
    file_path = Column(String, nullable=False)
    newcast_uid = Column(Integer, ForeignKey("newcast.uid"), nullable=False)
    newcast = relationship("NewcastModel", back_populates="articles")
