from dtos.write_disease_dto import DiseaseWriteDto
from typing import Iterable, List
from sqlalchemy.orm import Session
from fastapi import Depends
from ..dependencies.dbconnection import get_db
from ..dependencies.repositories import disease_repository, IDiseaseRepository
from ..models.disease import Disease


class DiseaseService:
    @staticmethod
    def get_all(
        db: Session = Depends(get_db),
        disease_repo: IDiseaseRepository = Depends(disease_repository),
    ):
        return disease_repo.get_all(db)

    @staticmethod
    def create(
        disease_dto: DiseaseWriteDto,
        db: Session = Depends(get_db),
        disease_repo: IDiseaseRepository = Depends(disease_repository),
    ):
        return disease_repo.save(db, **disease_dto.dict())

    @staticmethod
    def get_by_id(
        disease_id: int,
        db: Session = Depends(get_db),
        disease_repo: IDiseaseRepository = Depends(disease_repository),
    ):
        return disease_repo.find_by_id(db, disease_id)

    @staticmethod
    def delete(
        disease_id: int,
        db: Session = Depends(get_db),
        disease_repo: IDiseaseRepository = Depends(disease_repository),
    ):
        disease_repo.delete(db, disease_id)
