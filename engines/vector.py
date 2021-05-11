from math import log10, sqrt
from typing import Dict, List

import numpy as np
from tensorflow import keras

class VectorEngine:

    @staticmethod
    def compute_query_vector(index, query: List[str], alpha=0.5) -> Dict[str, float]:
        result: Dict[str, float] = {}
        frequency = {
            t: len(list(filter(lambda x: x == t, query)))
            for t in index.system_terms.keys()
        }
        max_freq = max(map(lambda t: frequency.get(t, 0), set(query)))

        for term, ni in index.system_terms.items():
            if term in query:
                try:
                    result[term] = (
                        alpha + (1 - alpha) * (frequency.get(term, 0) / max_freq)
                    ) * log10(index.total_documents / ni)
                except ZeroDivisionError:
                    result[term] = 0
            else:
                result[term] = 0

        return result

    @staticmethod
    def compute_doc_vector(index, doc: int) -> Dict[str, float]:
        result: Dict[str, float] = {}

        for term in index.system_terms.keys():
            result[term] = index.weight_function.get((term, doc), 0)

        return result

    @staticmethod
    def compute_sim(vquery: Dict[str, float], vdoc: Dict[str, float]) -> float:
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

        denominator = sqrt(sum(vdoc.get(t, 0.0) ** 2 for t in all_terms)) * sqrt(
            sum(vquery.get(t, 0.0) ** 2 for t in all_terms)
        )

        try:
            return numerator / denominator
        except ZeroDivisionError:
            return 0

    @staticmethod
    def keras_compute_sim(vquery: Dict[str, float], vdoc: Dict[str, float]) -> np.float:
        all_terms = set(vquery.keys()).union(set(vdoc.keys()))
        d_vector = np.array(list(vdoc.get(t, 0.0) for t in all_terms), dtype=np.float)
        q_vector = np.array(list(vquery.get(t, 0.0) for t in all_terms), dtype=np.float)

        return -keras.losses.cosine_similarity(d_vector, q_vector)