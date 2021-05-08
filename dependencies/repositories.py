from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from repositories.disease_repo import DiseaseRepository, JsonDiseaseRepository
from repositories.interface_disesease_repository import IDiseaseRepository

def disease_repository() -> IDiseaseRepository:
    # return DiseaseRepository()
    return JsonDiseaseRepository()