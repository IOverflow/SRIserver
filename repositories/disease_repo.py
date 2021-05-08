from databases.core import Database
import sqlalchemy
from sqlalchemy.orm import query
from dtos.disease_dtos import DiseaseReadDto
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from typing import Iterable, List, Mapping, Optional
from .interface_disesease_repository import IDiseaseRepository
import json
from dependencies.dbconnection import database
from models.models import diseases


class DiseaseRepository(IDiseaseRepository):

    def __init__(self, database: Database = database, table: sqlalchemy.Table = diseases):
        self.database = database
        self.table = table

    async def get_all(self, skip: int = 0, limit: int = 0) -> Iterable[DiseaseReadDto]:
        query = self.table.select()
        diseases = await self.database.fetch_all(query)
        return [DiseaseReadDto(**disease) for disease in diseases]

    async def find_by_id(self, id: int) -> Optional[DiseaseReadDto]:
        query = self.table.select().where(self.table.c.id==id)
        disease = await self.database.fetch_one(query)
        if disease:
            return DiseaseReadDto(**disease)
        else:
            return None

    async def save(self, **kwargs) -> int:
        query = self.table.insert().values(**kwargs)
        disease_id = await self.database.execute(query)
        return disease_id

    async def delete(self, id: int) -> None:
        query = self.table.delete().where(self.table.c.id == id)
        await self.database.execute(query)

    async def update(self, **kwargs) -> None:
        query = self.table.update().where(self.table.c.id == kwargs['id']).values(**kwargs)
        await self.database.execute(query)

class JsonDiseaseRepository(IDiseaseRepository):

    def __init__(self) -> None:
        self.file = 'diseases.json'

    async def get_all(self, skip: int = 0, limit: int = 0) -> Iterable[DiseaseReadDto]:
        result: List[DiseaseReadDto] = []
        with open(self.file, "br") as store:
            for data in json.loads(store.read().decode()):
                result.append(DiseaseReadDto(**data))
        return result

    async def find_by_id(self, id: int) -> Optional[DiseaseReadDto]:
        result: Optional[DiseaseReadDto] = None
        with open(self.file, "rb") as store:
            for data in json.loads(store.read().decode()):
                if data['id'] == id:
                    result = DiseaseReadDto(**data)
                    break
        return result

    async def save(self, **kwargs) -> DiseaseReadDto:
        store = open(self.file, "rb")
        data = json.loads(store.read().decode())
        newId = len(data) + 1
        kwargs['id'] = newId
        data.append(kwargs)
        store.close()
        store = open(self.file, "wb")
        store.write(json.dumps(data).encode())
        store.close()
        return DiseaseReadDto(**kwargs)
