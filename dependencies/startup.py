from services.disease_service import DiseaseService
from repositories.disease_repo import JsonDiseaseRepository


def get_disease_service():
    return DiseaseService(disease_repo=JsonDiseaseRepository())
