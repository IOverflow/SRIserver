from dtos.disease_dtos import DiseaseReadDto
from fastapi.param_functions import Depends
from dependencies.dbconnection import get_db
from sqlalchemy.orm.session import Session
from typing import Iterable, List, Optional
from .interface_disesease_repository import IDiseaseRepository
from models.models import Disease
import json


class DiseaseRepository(IDiseaseRepository):

    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 0) -> Iterable[Disease]:
        return self.db.query(Disease).offset(skip).limit(limit).all()

    def find_by_id(self, id: int) -> Optional[Disease]:
        return self.db.query(Disease).filter_by(id=id).first()

    def save(self, **kwargs) -> Disease:
        disease = Disease(**kwargs)
        self.db.add(disease)
        self.db.commit()
        self.db.refresh(disease)
        return disease

    def delete(self, id: int) -> None:
        disease = self.db.query(Disease).filter_by(id=id).first()
        if disease is not None:
            self.db.delete(disease)
            self.db.flush()

    def update(self, **kwargs) -> Disease:
        return Disease()

class JsonDiseaseRepository(IDiseaseRepository):

    def __init__(self) -> None:
        self.file = 'diseases.json'

    def get_all(self, skip: int = 0, limit: int = 0) -> Iterable[Disease]:
        result: List[Disease] = []
        with open(self.file, "br") as store:
            for data in json.loads(store.read().decode()):
                result.append(Disease(**data))
        return result

    def find_by_id(self, id: int) -> Optional[Disease]:
        result: Disease = Disease()
        with open(self.file, "rb") as store:
            for data in json.loads(store.read().decode()):
                if data['id'] == id:
                    result = Disease(**data)
                    break
        return result

    def save(self, **kwargs) -> Disease:
        store = open(self.file, "rb")
        data = json.loads(store.read().decode())
        newId = len(data) + 1
        kwargs['id'] = newId
        data.append(kwargs)
        store.close()
        store = open(self.file, "wb")
        store.write(json.dumps(data).encode())
        return Disease(**kwargs)
