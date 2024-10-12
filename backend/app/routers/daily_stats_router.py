from datetime import datetime, timedelta, timezone

from fastapi import APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.config.database_config import SessionLocal
from app.models.article_model import ArticleModel

router = APIRouter()


@router.get("/stats/last_week")
def get_last_week_stats():
    db: Session = SessionLocal()
    last_week_stats = (
        db.query(ArticleModel.upload_date, func.count(ArticleModel.id))
        .filter(
            ArticleModel.upload_date >= datetime.now(timezone.utc) - timedelta(days=7)
        )
        .group_by(ArticleModel.upload_date)
        .all()
    )

    db.close()
    return last_week_stats
