from sqlalchemy import Table
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer
from ..dependencies.dbconnection import Base

association_table = Table(
    "diseases_to_symptoms",
    Base.metadata,
    Column("symptom_id", Integer, ForeignKey('symptoms.id')),
    Column("disease_id", Integer, ForeignKey('diseases.id'))
)