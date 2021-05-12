from dtos.disease_dtos import DiseaseReadDto
from typing import List, Optional
from pydantic import BaseModel

class QueryTerms(BaseModel):
    query: str

    def get_terms(self) -> List[str]:
        return self.query.split()

class QueryResponse(BaseModel):
    diseases: Optional[List[DiseaseReadDto]] = []
    related: Optional[List[str]] = []

def query_dependency(query: str):
    return QueryTerms(query=query)