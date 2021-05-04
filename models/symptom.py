from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column
from sqlalchemy import Integer, String
from dependencies.dbconnection import Base
from .disease_symptom_table import association_table

class Symptom(Base):
    __tablename__ = "symptoms"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    diseases = relationship("Disease", secondary=association_table, back_populates="symptoms")