import ftplib
import os
import shutil
import zipfile
from datetime import date as _date

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models.article_model import ArticleModel
from app.models.newcast_model import NewcastModel
from app.models.stats_model import StatsModel
from app.services import stats_service
from app.utils import date_utils


def update_day_stats(
    newcast_uid: int, date: _date, articles_uploaded: int, db: Session
) -> StatsModel:
    day_stats = stats_service.get_stats_by_date(newcast_uid, date, db)

    if not day_stats:
        day_stats = StatsModel(
            date=date,
            articles_upload=0,
            day_of_week=date_utils.get_weekday(date),
            newcast_uid=newcast_uid,
        )
        db.add(day_stats)

    day_stats.articles_upload += articles_uploaded
    db.commit()
    db.refresh(day_stats)
    return day_stats


def handle_txt_upload(file: UploadFile, newcast: NewcastModel, db: Session) -> int:
    today = date_utils.get_today()
    folder = f"uploads/{newcast.name}/{today}"
    txt_file_path = f"{folder}/{file.filename}"
    os.makedirs(folder, exist_ok=True)

    with open(txt_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    news_article = ArticleModel(
        upload_date=today,
        file_path=f"{txt_file_path}",
        newcast_uid=newcast.uid,
    )
    db.add(news_article)
    db.commit()
    return 1


def delete_nested_folders(folder: str):
    for root, dirs, files in os.walk(folder):
        if root != folder:
            for file in files:
                source_path = os.path.join(root, file)
                dest_path = os.path.join(folder, file)
                shutil.move(source_path, dest_path)

    for root, dirs, _ in os.walk(folder, topdown=False):
        for _dir in dirs:
            dir_path = os.path.join(root, _dir)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)


def handle_zip_upload(file: UploadFile, newcast: NewcastModel, db: Session) -> int:
    today = date_utils.get_today()
    folder = f"uploads/{newcast.name}/{today}"
    os.makedirs(folder, exist_ok=True)
    zip_file_path = f"{folder}/{file.filename}"
    article_count = 0

    with open(zip_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        os.makedirs(f"{folder}/{newcast.name}", exist_ok=True)
        zip_ref.extractall(f"{folder}/{newcast.name}")
        file_list = zip_ref.namelist()
        zip_files = [f for f in file_list if not zip_ref.getinfo(f).is_dir()]
        article_count = len(zip_files)
        delete_nested_folders(folder)
        for filename in zip_ref.namelist():
            news_article = ArticleModel(
                upload_date=today,
                file_path=f"{folder}/{filename}",
                newcast_uid=newcast.uid,
            )
            db.add(news_article)

    os.remove(zip_file_path)
    db.commit()
    return article_count


# TODO: PENDING
def download_files_from_ftp(
    ftp_host: str, ftp_user: str, ftp_pass: str, local_directory: str
):
    """Download files from the FTP server to the local directory."""
    ftp = ftplib.FTP(ftp_host)
    ftp.login(ftp_user, ftp_pass)
    ftp.cwd("/")
    os.makedirs(local_directory, exist_ok=True)
    filenames = ftp.nlst()

    for filename in filenames:
        local_filepath = os.path.join(local_directory, filename)
        with open(local_filepath, "wb") as local_file:
            ftp.retrbinary(f"RETR {filename}", local_file.write)

    ftp.quit()
    return filenames
