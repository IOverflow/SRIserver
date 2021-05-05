from dtos.disease_dtos import DiseaseWriteDto
from fastapi import Depends
from dependencies.repositories import disease_repository, IDiseaseRepository


class DiseaseService:
    def __init__(self, disease_repo: IDiseaseRepository = Depends(disease_repository)):
        self.disease_repo = disease_repo

    def get_all(self):
        return self.disease_repo.get_all()

    def create(self, disease_dto: DiseaseWriteDto):
        return self.disease_repo.save(**disease_dto.dict(exclude_unset=True))

    def get_by_id(self, disease_id: int):
        return self.disease_repo.find_by_id(disease_id)

    def delete(self, disease_id: int):
        self.disease_repo.delete(disease_id)
