from dependencies.repositories import disease_repository
from repositories.interface_disesease_repository import IDiseaseRepository
from dependencies.dbconnection import get_db
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from services.disease_service import DiseaseService


def get_disease_service(
    db: Session = Depends(get_db),
    repo: IDiseaseRepository = Depends(disease_repository),
):
    return DiseaseService(db, repo)
