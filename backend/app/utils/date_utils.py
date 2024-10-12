from datetime import date as _date
from datetime import datetime
from typing import Union

from app.constants.enums.week_day import WeekDay
from app.constants.formats import DATE_FORMAT


def get_weekday(date: Union[datetime, _date]) -> str:
    week_day = date.weekday()
    week_day_list = list(WeekDay)
    return week_day_list[week_day].value


def get_today() -> _date:
    return datetime.now().date()
