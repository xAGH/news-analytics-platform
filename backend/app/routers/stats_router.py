from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.ioc.dependencies import get_db
from app.services import stats_service
from app.utils import responses

router = APIRouter()


@router.get("/stats/{newcast_uid}/last_week")
def get_last_week_stats(newcast_uid: int, db: Annotated[Session, Depends(get_db)]):
    week_stats = stats_service.get_last_week_stats(newcast_uid, db)
    model = [
        {
            "date": str(stats.date),
            "articles_upload": stats.articles_upload,
            "day_of_week": stats.day_of_week.value,
            "uid": stats.uid,
        }
        for stats in week_stats
    ]
    return responses.ok(data=model, message="Weekly stats obtained successfully")
