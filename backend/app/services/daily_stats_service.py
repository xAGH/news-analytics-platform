from datetime import date as _date
from datetime import datetime
from typing import Optional, Union

from sqlalchemy.orm import Session

from app.models.daily_stats_model import DailyStatsModel


def get_daily_stats_by_date(
    date: Union[datetime, _date], db: Session
) -> Optional[DailyStatsModel]:
    if isinstance(date, datetime):
        date = date.date()
    return db.query(DailyStatsModel).filter(DailyStatsModel.date == date).first()
