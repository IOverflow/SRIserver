from sqlalchemy.orm.session import Session
from typing import Iterable, Optional
from .interface_symptom_repo import ISymptomRepository
from ..models.symptom import Symptom


class SymptomRepository(ISymptomRepository):
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 0) -> Iterable[Symptom]:
        return db.query(Symptom).offset(skip).limit(limit).all()

    @staticmethod
    def find_by_id(db: Session, id: int) -> Optional[Symptom]:
        return db.query(Symptom).filter_by(id=id).first()

    @staticmethod
    def save(db: Session, **kwargs) -> Symptom:
        symptom = Symptom(**kwargs)
        db.add(symptom)
        db.commit()
        db.refresh(symptom)
        return symptom

    @staticmethod
    def delete(db: Session, id: int) -> None:
        symptom = db.query(Symptom).filter_by(id=id).first()
        if symptom is not None:
            db.delete(symptom)
            db.flush()

    @staticmethod
    def update(db: Session, **kwargs) -> Symptom:
        return Symptom()