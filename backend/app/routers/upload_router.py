from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.ioc.dependencies import get_db
from app.services import newcast_service, upload_service
from app.utils import responses

router = APIRouter()


@router.post("/upload/{newcast_uid}")
async def upload_zip(
    newcast_uid: int,
    file: UploadFile,
    db: Annotated[Session, Depends(get_db)],
):
    is_zip = file.filename.endswith(".zip")
    is_txt = file.filename.endswith(".txt")

    if not is_zip and not is_txt:
        return responses.bad_request(
            "Invalid file format. Please upload a txt or zip file"
        )

    newcast = newcast_service.get_newcast_by_uid(newcast_uid, db)
    params = (file, newcast, db)

    if not newcast:
        return responses.not_found("Newspaper not found")

    if is_zip:
        uploaded_articles = upload_service.handle_zip_upload(*params)
    else:
        uploaded_articles = upload_service.handle_txt_upload(*params)

    return responses.ok(
        message=f"{uploaded_articles} articles have been uploaded today"
    )
