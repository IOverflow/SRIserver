from dependencies.startup import get_disease_service
from typing import Dict, Tuple
from fastapi import FastAPI
import loaders
from controllers.disease_controller import disease_controller
from controllers.search_controller import search_controller
from services.search_service import index
from math import log10
from colorama import Fore
import uvicorn
import config.settings as conf

# Initialize database here
# loaders.load_database()

app = FastAPI()


@app.on_event("startup")
async def make_index():
    """
    Create the index for search engine.
    """
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
    print(f"{Fore.GREEN}INFO{Fore.RESET}:     Index created")


# Load controllers here
app.include_router(disease_controller)
app.include_router(search_controller)

if __name__ == "__main__":
    uvicorn.run(app, host=conf.HOST_IP, port=conf.HOST_PORT)
