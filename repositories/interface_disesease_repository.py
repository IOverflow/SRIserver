from abc import ABC
from typing import Iterable, List, Optional

from sqlalchemy.orm.session import Session
from models.disease import Disease

class IDiseaseRepository(ABC):

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 0) -> Iterable[Disease]:
        return []

    @staticmethod
    def find_by_id(db: Session, id: int) -> Optional[Disease]:
        return Disease()

    @staticmethod
    def save(db: Session, **kwargs) -> Disease:
        return Disease()

    @staticmethod
    def delete(db: Session, id: int) -> None:
        pass

    @staticmethod
    def update(db: Session, **kwargs) -> Disease:
        return Disease()
