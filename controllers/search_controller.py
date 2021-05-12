from dtos.disease_dtos import DiseaseReadDto
from typing import List, Optional
from fastapi import APIRouter
from fastapi.param_functions import Depends, Query
from services.search_service import SearchService
from dtos.query_dtos import QueryTerms, query_dependency

search_controller = APIRouter(prefix="/search")


@search_controller.get("/ranked", response_model=List[DiseaseReadDto])
async def search(q: QueryTerms = Depends(query_dependency), search_service: SearchService = Depends()):
    return await search_service.search(q)

@search_controller.get("/vocabulary", response_model=List[str])
async def vocabulary(search_service: SearchService = Depends()):
    return search_service.get_all_index_terms()

@search_controller.get("/")
async def ranked_search(q: QueryTerms = Depends(query_dependency), search_service: SearchService = Depends()):
    return await search_service.raw_search(q)
