from dtos.query_dtos import QueryTerms
from services.disease_service import DiseaseService
from typing import Dict, List, Tuple
from models.models import Disease

from fastapi.param_functions import Depends


class Index:
    def __init__(self) -> None:
        self.weight_function: Dict[Tuple[str, int], float] = {}
        self.system_terms: Dict[str, int] = {}
        self.total_documents: int = 0

    def __call__(self):
        return self


index = Index()


class SerchService:

    # Use Dependency Injection here on services that this might depend
    def __init__(
        self,
        indx: Index = Depends(index),
        disease_service: DiseaseService = Depends(),
    ):
        self.index = indx
        self.disease_service = disease_service

    def search(self, query: QueryTerms) -> List[Disease]:
        return []
