from sqlalchemy.orm.session import Session
from typing import Iterable, Optional
from .interface_disesease_repository import IDiseaseRepository
from models.disease import Disease


class DiseaseRepository(IDiseaseRepository):
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 0) -> Iterable[Disease]:
        return db.query(Disease).offset(skip).limit(limit).all()

    @staticmethod
    def find_by_id(db: Session, id: int) -> Optional[Disease]:
        return db.query(Disease).filter_by(id=id).first()

    @staticmethod
    def save(db: Session, **kwargs) -> Disease:
        disease = Disease(**kwargs)
        db.add(disease)
        db.commit()
        db.refresh(disease)
        return disease

    @staticmethod
    def delete(db: Session, id: int) -> None:
        disease = db.query(Disease).filter_by(id=id).first()
        if disease is not None:
            db.delete(disease)
            db.flush()

    @staticmethod
    def update(db: Session, **kwargs) -> Disease:
        return Disease()