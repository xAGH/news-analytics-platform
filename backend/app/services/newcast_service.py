from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.newcast_model import NewcastModel
from app.schemas.newcast_schema import NewcastCreate


def get_newcast_by_uid(uid: int, db: Session) -> Optional[NewcastModel]:
    return db.query(NewcastModel).filter(NewcastModel.uid == uid).first()


def get_newcast_by_name(name: str, db: Session) -> Optional[NewcastModel]:
    return db.query(NewcastModel).filter(NewcastModel.name == name).first()


def create_newcast(newcast: NewcastCreate, db: Session) -> NewcastModel:
    db_newcast = NewcastModel(name=newcast.name)
    db.add(db_newcast)
    db.commit()
    return db_newcast


def get_all_newcasts(db: Session) -> List[NewcastModel]:
    return db.query(NewcastModel).all()
