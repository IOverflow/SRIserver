from dependencies.dbconnection import get_db
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from repositories.disease_repo import DiseaseRepository, JsonDiseaseRepository
from repositories.interface_disesease_repository import IDiseaseRepository
from repositories.interface_symptom_repo import ISymptomRepository
from repositories.symptom_repo import SymptomRepository


def symptom_repository() -> ISymptomRepository:
    return SymptomRepository()


# def disease_repository(db: Session = Depends(get_db)) -> IDiseaseRepository:
#     # return DiseaseRepository(db)
#     return JsonDiseaseRepository()


def disease_repository():
    return JsonDiseaseRepository()
