from typing import Iterable, List
from dtos.disease_dtos import DiseaseReadDto, DiseaseWriteDto
from fastapi import Depends
from dependencies.repositories import disease_repository, IDiseaseRepository


class DiseaseService:
    def __init__(self, disease_repo: IDiseaseRepository = Depends(disease_repository)):
        self.disease_repo = disease_repo

    async def get_all(self) -> Iterable[DiseaseReadDto]:
        return await self.disease_repo.get_all()

    async def create(self, disease_dto: DiseaseWriteDto) -> DiseaseReadDto:
        return await self.disease_repo.save(**disease_dto.dict(exclude_unset=True))

    async def get_by_id(self, disease_id: int):
        return await self.disease_repo.find_by_id(disease_id)

    async def delete(self, disease_id: int):
        await self.disease_repo.delete(disease_id)
