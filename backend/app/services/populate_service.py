from datetime import timedelta
from random import randint
from typing import Optional

from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import Session

from app.models.stats_model import StatsModel
from app.schemas.populate_schema import Populate
from app.utils import date_utils


def populate(populate_data: Populate, db: Session) -> Optional[str]:
    today = date_utils.get_today()
    date_ago = today - relativedelta(months=populate_data.months_to_populate)
    days = (today - date_ago).days
    stats = []
    for day in range(days + 1):
        date = date_ago + timedelta(days=day)
        articles_uploaded = randint(
            populate_data.min_articles_per_day, populate_data.max_articles_per_day
        )
        day_stats = StatsModel(
            date=date,
            articles_upload=articles_uploaded,
            day_of_week=date_utils.get_weekday(date),
            newcast_uid=populate_data.newcast_uid,
        )
        stats.append(day_stats)
    db.add_all(stats)
    db.commit()
