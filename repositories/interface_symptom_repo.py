from abc import ABC
from typing import Iterable, List, Optional

from sqlalchemy.orm.session import Session
from models.symptom import Symptom

class ISymptomRepository(ABC):

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 0) -> Iterable[Symptom]:
        return []

    @staticmethod
    def find_by_id(db: Session, id: int) -> Optional[Symptom]:
        return Symptom()

    @staticmethod
    def save(db: Session, **kwargs) -> Symptom:
        return Symptom()

    @staticmethod
    def delete(db: Session, id: int) -> None:
        pass

    @staticmethod
    def update(db: Session, **kwargs) -> Symptom:
        return Symptom()
