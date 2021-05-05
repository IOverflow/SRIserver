from typing import List, Optional
from pydantic import BaseModel

class DiseaseWriteDto(BaseModel):
    name: str
    description: str
    treatment: str

    class Config:
        orm_mode = True