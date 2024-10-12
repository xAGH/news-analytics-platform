import math
from collections import Counter
from datetime import date as _date
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Union

import numpy as np
from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import Session

from app.models.stats_model import StatsModel
from app.utils import date_utils


def get_stats_by_date(
    newcast_uid: int, date: Union[datetime, _date], db: Session
) -> Optional[StatsModel]:
    if isinstance(date, datetime):
        date = date.date()
    return (
        db.query(StatsModel)
        .filter(StatsModel.date == date)
        .filter(StatsModel.newcast_uid == newcast_uid)
        .first()
    )


def get_last_week_stats(newcast_uid: int, db: Session) -> List[StatsModel]:
    today = date_utils.get_today()
    start_of_week = today - timedelta(days=today.weekday())
    results = (
        db.query(StatsModel)
        .filter(StatsModel.date >= start_of_week)
        .filter(StatsModel.newcast_uid == newcast_uid)
        .all()
    )
    return results


def get_months_ago_data_by_week_day(
    newcast_uid: int, week_day: str, months: int, db: Session
) -> List[StatsModel]:
    today = date_utils.get_today()
    months_ago = today - relativedelta(months=months)
    average_uploads = (
        db.query(StatsModel)
        .filter(StatsModel.date >= months_ago)
        .filter(StatsModel.day_of_week == week_day)
        .filter(StatsModel.newcast_uid == newcast_uid)
    )
    return average_uploads


def calculate_variation_coefficient(
    avg_uploads: float, uploads: int
) -> Tuple[float, float, float]:
    variance = sum((x - avg_uploads) ** 2 for x in uploads) / len(uploads)
    standard_deviation = math.sqrt(variance)
    variation_coefficient = (standard_deviation / avg_uploads) * 100
    return variance, standard_deviation, variation_coefficient


def get_interquartile_range(uploads: List[int]):
    sorted_uploads = sorted(uploads)
    q1 = np.percentile(sorted_uploads, 25)
    q3 = np.percentile(sorted_uploads, 75)
    iqr = q3 - q1
    return iqr


def apply_statistic_model(
    avg_uploads: float, uploads: int
) -> Tuple[bool, Dict[str, float]]:
    statistics = calculate_variation_coefficient(avg_uploads, uploads)
    variance, standard_deviation, variation_coefficient = statistics
    is_normal: bool
    extra_data = dict()
    last_upload = uploads[-1]

    if variation_coefficient >= 25:
        iqr = get_interquartile_range(uploads)
        is_normal = bool(last_upload > iqr)
        extra_data = dict(interquartil_range=iqr)

    else:
        frequency_table = Counter(uploads)
        most_common_upload = frequency_table.most_common(1)[0]
        is_normal = last_upload >= most_common_upload[0]

    data = dict(
        variance=variance,
        standard_deviation=standard_deviation,
        variation_coefficient=variation_coefficient,
    )
    data.update(extra_data)

    return is_normal, data


def get_stats_data(
    newcast_uid: int, uploaded_now: int, uploaded_today: int, db: Session
) -> Tuple[Dict[str, Union[str, int]], str]:
    today = date_utils.get_today()
    week_day = date_utils.get_weekday(today)
    months_ago_data = get_months_ago_data_by_week_day(newcast_uid, week_day, 6, db)
    uploads = [article.articles_upload for article in months_ago_data]
    avg_uploads = sum(uploads) / len(uploads)
    is_normal_upload = (avg_uploads * 0.8) <= uploaded_now
    extra_data = dict()

    if not is_normal_upload:
        is_normal_upload, extra_data = apply_statistic_model(avg_uploads, uploads)

    normal_message = "The number of articles uploaded is within the acceptable range."
    low_articles_message = "The number of articles uploaded is below the usual level, attention is required."
    notification = (normal_message if is_normal_upload else low_articles_message,)
    data = dict(
        is_normal_upload=is_normal_upload,
        uploaded_now=uploaded_now,
        uploaded_today=uploaded_today,
        avgerage_upload=int(avg_uploads),
    )
    data.update(extra_data)
    return data, notification
