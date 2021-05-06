from typing import List
from pydantic import BaseModel

class QueryTerms(BaseModel):
    query: str

    def get_terms(self) -> List[str]:
        return self.query.split()

def query_dependency(query: str):
    return QueryTerms(query=query)