from abc import ABC
from typing import Iterable, List, Optional
from dependencies.dbconnection import database
from dtos.disease_dtos import DiseaseReadDto

class IDiseaseRepository(ABC):

    async def get_all(self, skip: int = 0, limit: int = 0) -> Iterable[DiseaseReadDto]:
        return []

    async def find_by_id(self, id: int) -> Optional[DiseaseReadDto]:
        return DiseaseReadDto()

    async def save(self, **kwargs) -> DiseaseReadDto:
        return DiseaseReadDto()

    async def delete(self, id: int) -> None:
        pass

    async def update(self, **kwargs) -> DiseaseReadDto:
        return DiseaseReadDto()
