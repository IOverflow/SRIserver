from dtos.disease_dtos import DiseaseReadDto
from typing import List
from fastapi import APIRouter
from fastapi.param_functions import Depends
from services.search_service import SearchService
from dtos.query_dtos import QueryTerms

search_controller = APIRouter(prefix="/search")


@search_controller.get("/", response_model=List[DiseaseReadDto])
async def search(query: QueryTerms, search_service: SearchService = Depends()):
    return search_service.search(query)
