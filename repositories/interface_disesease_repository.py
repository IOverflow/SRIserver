from abc import ABC
from dependencies.dbconnection import get_db
from typing import Iterable, List, Optional
from fastapi import Depends
from sqlalchemy.orm.session import Session
from models.models import Disease

class IDiseaseRepository(ABC):

    def get_all(self, skip: int = 0, limit: int = 0) -> Iterable[Disease]:
        return []

    def find_by_id(self, id: int) -> Optional[Disease]:
        return Disease()

    def save(self, **kwargs) -> Disease:
        return Disease()

    def delete(self, id: int) -> None:
        pass

    def update(self, **kwargs) -> Disease:
        return Disease()
