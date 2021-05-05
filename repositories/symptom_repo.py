from dependencies.dbconnection import get_db
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from typing import Iterable, Optional
from .interface_symptom_repo import ISymptomRepository
from models.models import Symptom


class SymptomRepository(ISymptomRepository):
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 0) -> Iterable[Symptom]:
        return self.db.query(Symptom).offset(skip).limit(limit).all()

    def find_by_id(self, id: int) -> Optional[Symptom]:
        return self.db.query(Symptom).filter_by(id=id).first()

    def save(self, **kwargs) -> Symptom:
        symptom = Symptom(**kwargs)
        self.db.add(symptom)
        self.db.commit()
        self.db.refresh(symptom)
        return symptom

    def delete(self, id: int) -> None:
        symptom = self.db.query(Symptom).filter_by(id=id).first()
        if symptom is not None:
            self.db.delete(symptom)
            self.db.flush()

    def update(self, **kwargs) -> Symptom:
        return Symptom()
