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

    def compute_query_vector(self, query: List[str]) -> Dict[str, float]:
        return {}

    def compute_doc_vector(self, doc: int) -> Dict[str, float]:
        return {}

    def compute_sim(self, vquery: Dict[str, float], vdoc: Dict[str, float]) -> float:
        return 0.0

    def __call__(self):
        return self


index = Index()


class SearchService:

    # Use Dependency Injection here on services that this might depend
    def __init__(
        self,
        indx: Index = Depends(index),
        disease_service: DiseaseService = Depends(),
    ):
        self.index = indx
        self.disease_service = disease_service

    def search(self, query: QueryTerms) -> List[Disease]:
        query_vector = self.index.compute_query_vector(query.get_terms())
        docs = set(map(lambda td: td[1], index.weight_function.keys()))
        sim_doc_pair: List[Tuple[float, int]] = []

        for doc in docs:
            vdoc = index.compute_doc_vector(doc)
            similarity = index.compute_sim(query_vector, vdoc)
            sim_doc_pair.append((similarity, doc))

        # order similarity list in descending order
        search_resul = list(
            map(
                lambda sd: self.disease_service.get_by_id(sd[1]) or Disease(),
                sorted(sim_doc_pair, reverse=True),
            )
        )
        
        return search_resul
