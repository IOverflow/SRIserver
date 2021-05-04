from repositories.disease_repo import DiseaseRepository
from repositories.interface_disesease_repository import IDiseaseRepository
from repositories.interface_symptom_repo import ISymptomRepository
from repositories.symptom_repo import SymptomRepository

def symptom_repository() -> ISymptomRepository:
    return SymptomRepository()

def disease_repository() -> IDiseaseRepository:
    return DiseaseRepository()