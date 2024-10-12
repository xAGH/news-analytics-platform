from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.ioc.dependencies import get_db
from app.schemas.newcast_schema import NewcastCreate
from app.services import newcast_service
from app.utils import responses

router = APIRouter()


@router.post("/newcast")
async def create_newcast(
    newcast_create: NewcastCreate, db: Annotated[Session, Depends(get_db)]
):
    newcast = newcast_service.get_newcast_by_name(newcast_create.name, db)

    if newcast:
        return responses.conflict(
            f"A newscast with name {newcast_create.name} already exists"
        )

    newcast = newcast_service.create_newcast(newcast_create, db)
    newcast_created = {
        "name": newcast.name,
        "uid": newcast.uid,
        "created_at": str(newcast.created_at),
    }
    return responses.created(message=f"Newscast created", data=newcast_created)


@router.get("/newcast")
async def get_newcasts(db: Annotated[Session, Depends(get_db)]):
    newcasts = newcast_service.get_all_newcasts(db)

    newcast_models = [
        {
            "name": newcast.name,
            "uid": newcast.uid,
            "created_at": str(newcast.created_at),
        }
        for newcast in newcasts
    ]

    return responses.created(message=f"Newscasts obtained", data=newcast_models)
