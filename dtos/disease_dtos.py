from typing import List, Optional
from pydantic import BaseModel

class DiseaseReadDto(BaseModel):
    id: int
    name: str
    description: str
    treatment: str
    symptoms: Optional[List[int]]

    class Config:
        orm_mode = True


class DiseaseWriteDto(BaseModel):
    name: str
    description: str
    treatment: str

    class Config:
        orm_mode = True