from dtos.write_disease_dto import DiseaseWriteDto
from typing import List
from fastapi import APIRouter
from fastapi.param_functions import Depends
from dependencies.services import DiseaseService, get_disease_service
from dtos.read_disease_dto import DiseaseReadDto

disease_controller = APIRouter(prefix="/disease")


@disease_controller.get("/", response_model=List[DiseaseReadDto])
def get(disease_service: DiseaseService = Depends(get_disease_service)):
    return disease_service.get_all()


@disease_controller.get("/{id}", response_model=DiseaseReadDto)
def get_id(
    id: int,
    disease_service: DiseaseService = Depends(get_disease_service),
):
    return disease_service.get_by_id(id)


@disease_controller.post("/create", response_model=DiseaseReadDto)
def create(
    disease: DiseaseWriteDto,
    disease_service: DiseaseService = Depends(get_disease_service),
):
    return disease_service.create(disease)
