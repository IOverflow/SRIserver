import numpy as np
from engines.ranking.nn_model import FeedForwardRankingNNModel, ranker
from dtos.disease_dtos import DiseaseReadDto
from pandas.io import json
from dependencies.startup import get_disease_service
from dtos.query_dtos import QueryTerms
from services.disease_service import DiseaseService
from typing import Dict, Iterable, List, Tuple
from math import log10, sqrt
from colorama import Fore
from engines.vector import VectorEngine

from fastapi.param_functions import Depends


class Index:
    def __init__(self) -> None:
        self.weight_function: Dict[Tuple[str, int], float] = {}
        self.system_terms: Dict[str, int] = {}
        self.total_documents: int = 0

    @staticmethod
    async def initialize(index: "Index"):
        disease_service = get_disease_service()
        diseases = await disease_service.get_all()
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


    def __call__(self):
        return self


index = Index()


class SearchService:

    # Use Dependency Injection here on services that this might depend
    def __init__(
        self,
        indx: Index = Depends(index),
        disease_service: DiseaseService = Depends(),
        ranker: FeedForwardRankingNNModel = Depends(ranker)
    ):
        self.index = indx
        self.disease_service = disease_service

    async def raw_search(self, query: QueryTerms) -> List[DiseaseReadDto]:
        query_vector = VectorEngine.compute_query_vector(self.index, query.get_terms())
        docs = set(map(lambda td: td[1], self.index.weight_function.keys()))
        sim_doc_pair: List[Tuple[float, int]] = []

        for doc in docs:
            vdoc = VectorEngine.compute_doc_vector(self.index, doc)
            similarity = VectorEngine.keras_compute_sim(query_vector, vdoc)
            if similarity > 0:
                sim_doc_pair.append((similarity, doc))


        # order similarity list in descending order
        search_result = [
            (await self.disease_service.get_by_id(sd[1])) or DiseaseReadDto()
            for sd in sorted(sim_doc_pair, reverse=True)
        ]

        return search_result

    async def search(self, query: QueryTerms, v2search=False) -> List[DiseaseReadDto]:
        query_vector = VectorEngine.compute_query_vector(self.index, query.get_terms())
        docs = set(map(lambda td: td[1], self.index.weight_function.keys()))
        sim_doc_pair: List[Tuple[float, int]] = []
        l: List[float] = []

        for doc in docs:
            vdoc = VectorEngine.compute_doc_vector(self.index, doc)
            if not v2search:
                similarity = VectorEngine.compute_sim(query_vector, vdoc)
            else:
                similarity = VectorEngine.keras_compute_sim(query_vector, vdoc)
            # if similarity > 0:
            l.append(similarity)

        # Pass the similarity vector through the ranker engine
        doc_vector: np.ndarray = np.array(l)
        q_vector: np.ndarray = np.array(list(query_vector.values()))
        sim_vector: np.ndarray = ranker.compute(doc_vector, q_vector)

        print(sim_vector)

        for doc, sim in zip(docs, sim_vector[0]):
            if sim >= 0.2:
                sim_doc_pair.append((sim, doc))

        # order similarity list in descending order
        search_result = [
            (await self.disease_service.get_by_id(sd[1])) or DiseaseReadDto()
            for sd in sorted(sim_doc_pair, reverse=True)
        ]

        return search_result

    def get_all_index_terms(self) -> Iterable[str]:
        return list(self.index.system_terms.keys())
