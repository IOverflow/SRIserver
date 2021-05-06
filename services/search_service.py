from dependencies.startup import get_disease_service
from dtos.query_dtos import QueryTerms
from services.disease_service import DiseaseService
from typing import Dict, List, Tuple
from models.models import Disease
from math import log10, sqrt

from fastapi.param_functions import Depends


class Index:
    def __init__(self) -> None:
        self.weight_function: Dict[Tuple[str, int], float] = {}
        self.system_terms: Dict[str, int] = {}
        self.total_documents: int = 0

    @staticmethod
    def initialize(index: "Index"):
        disease_service = get_disease_service()
        diseases = disease_service.get_all()
        freq: Dict[Tuple[str, int], int] = {}
        idf: Dict[str, float] = {}
        system_terms: Dict[str, int] = {}
        tf: Dict[Tuple[str, int], float] = {}

        # Compute tf frequencies
        for disease in diseases:
            terms = disease.get_terms()
            unique_terms = set(terms)
            for term in unique_terms:
                freq[(term, disease.id)] = len(list(filter(lambda x: x == term, terms)))
                try:
                    system_terms[term] += 1
                except KeyError:
                    system_terms[term] = 1

        # Compute TFij
        for (term, doc), frequency in freq.items():
            # Get the maximum frequency of all terms in doc
            max_freq = max(
                map(
                    lambda tfd: tfd[1],
                    filter(lambda tfd: tfd[0][1] == doc, freq.items()),
                )
            )
            tf[term, doc] = frequency / max_freq

        # Compute idf
        N = len(list(diseases))
        for term, ni in system_terms.items():
            try:
                idf[term] = log10(N / ni)
            except ZeroDivisionError:
                idf[term] = 0

        # Compute weigths for each (document, term) pair
        for (term, doc), tfij in tf.items():
            index.weight_function[term, doc] = tfij * idf[term]

        index.system_terms = system_terms.copy()
        index.total_documents = N

    def compute_query_vector(self, query: List[str], alpha=0.5) -> Dict[str, float]:
        result: Dict[str, float] = {}
        frequency = {t: len(list(filter(lambda x: x == t, query))) for t in set(query)}
        max_freq = max(map(lambda t: frequency.get(t, 0), set(query)))

        for term, ni in self.system_terms.items():
            result[term] = (alpha + (1 - alpha) * (frequency.get(term, 0) / max_freq)) * log10(self.total_documents / ni)

        return result

    def compute_doc_vector(self, doc: int) -> Dict[str, float]:
        result: Dict[str, float] = {}
        
        for term in self.system_terms.keys():
            try:
                result[term] = self.weight_function[term, doc]
            except KeyError:
                pass

        return result

    def compute_sim(self, vquery: Dict[str, float], vdoc: Dict[str, float]) -> float:
        all_terms = set(vquery.keys()).union(set(vdoc.keys()))

        numerator = sum(
            list(
                wij * wiq
                for wij, wiq in zip(
                    list(vdoc.get(t, 0.0) for t in all_terms),
                    list(vquery.get(t, 0.0) for t in all_terms),
                )
            )
        )
        
        denominator = sqrt(sum(vdoc.get(t, 0.)**2 for t in all_terms)) * sqrt(sum(vquery.get(t, 0.0)**2 for t in all_terms))
        
        return numerator / denominator

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
        search_result = list(
            map(
                lambda sd: self.disease_service.get_by_id(sd[1]) or Disease(),
                sorted(sim_doc_pair, reverse=True),
            )
        )

        return search_result
