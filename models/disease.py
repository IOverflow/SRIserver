from typing import Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column
from sqlalchemy import Integer, Text
from dependencies.dbconnection import Base
from .disease_symptom_table import association_table

class Disease(Base):
    __tablename__ = "diseases"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text)
    treatment = Column(Text)
    symptoms = relationship("Symptom", secondary=association_table, back_populates="diseases")