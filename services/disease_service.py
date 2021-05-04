from dtos.write_disease_dto import DiseaseWriteDto
from typing import Iterable, List
from sqlalchemy.orm import Session
from fastapi import Depends
from dependencies.dbconnection import get_db
from dependencies.repositories import disease_repository, IDiseaseRepository
from models.disease import Disease


class DiseaseService:
    def __init__(self, db: Session, disease_repo: IDiseaseRepository):
        self.db = db
        self.disease_repo = disease_repo

    def get_all(self):
        return self.disease_repo.get_all(self.db)

    def create(self, disease_dto: DiseaseWriteDto):
        return self.disease_repo.save(self.db, **disease_dto.dict())

    def get_by_id(self, disease_id: int):
        return self.disease_repo.find_by_id(self.db, disease_id)

    def delete(self, disease_id: int):
        self.disease_repo.delete(self.db, disease_id)
