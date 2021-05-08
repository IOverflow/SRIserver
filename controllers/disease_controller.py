from services.disease_service import DiseaseService
from typing import List
from fastapi import APIRouter
from fastapi.param_functions import Depends
from dtos.disease_dtos import DiseaseReadDto, DiseaseWriteDto

disease_controller = APIRouter(prefix="/disease")


@disease_controller.get("/", response_model=List[DiseaseReadDto])
async def get(disease_service: DiseaseService = Depends()):
    return await disease_service.get_all()


@disease_controller.get("/{id}", response_model=DiseaseReadDto)
async def get_id(id: int, disease_service: DiseaseService = Depends()):
    return await disease_service.get_by_id(id)


@disease_controller.post("/create", response_model=DiseaseReadDto)
async def create(disease: DiseaseWriteDto, disease_service: DiseaseService = Depends()):
    return await disease_service.create(disease)
