from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy import Integer, String, Text, Numeric
from dependencies.dbconnection import Base

class Symptom(Base):
    __tablename__ = "symptoms"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    diseases = relationship("Disease", secondary='symptomDisease')

class Disease(Base):
    __tablename__ = "diseases"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(Text)
    treatment = Column(Text)
    symptoms = relationship("Symptom", secondary='symptomDisease')

class SymptomDisease(Base):
    __tablename__ = "symptomDisease"
    id = Column(Integer, primary_key=True)
    disease_id = Column(Integer, ForeignKey("diseases.id"))
    symptom_id = Column(Integer, ForeignKey("symptoms.id"))
    relevance = Column(Numeric, default=0.)

    disease = relationship("Disease", backref=backref("relevances", cascade="all, delete-orphan"))
    symptom = relationship("Symptom", backref=backref("relevances", cascade="all, delete-orphan"))