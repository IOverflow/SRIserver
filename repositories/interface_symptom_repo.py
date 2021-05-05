from abc import ABC
from dependencies.dbconnection import get_db
from typing import Iterable, List, Optional
from fastapi.param_functions import Depends

from sqlalchemy.orm.session import Session
from models.models import Symptom

class ISymptomRepository(ABC):

    def get_all(self, skip: int = 0, limit: int = 0) -> Iterable[Symptom]:
        return []

    def find_by_id(self, id: int) -> Optional[Symptom]:
        return Symptom()

    def save(self, **kwargs) -> Symptom:
        return Symptom()

    def delete(self, id: int) -> None:
        pass

    def update(self, **kwargs) -> Symptom:
        return Symptom()
