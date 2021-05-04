from typing import List, Optional
from pydantic import BaseModel

class DiseaseReadDto(BaseModel):
    description: str
    treatment: str
    symptoms: Optional[List[int]]

    class Config:
        orm_mode = True