from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.ioc.dependencies import get_db
from app.schemas.populate_schema import Populate
from app.services import newcast_service, populate_service
from app.utils import responses

router = APIRouter()


@router.post("/populate")
def populate_articles(populate_data: Populate, db: Annotated[Session, Depends(get_db)]):
    newcast = newcast_service.get_newcast_by_uid(populate_data.newcast_uid, db)

    if not newcast:
        return responses.not_found("Newcast not found")

    populate_service.populate(populate_data, db)
    return responses.ok(message="Populate stats table successfully")
