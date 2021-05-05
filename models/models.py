from typing import List
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy import Integer, String, Text, Numeric
from dependencies.dbconnection import Base

class Symptom(Base):
    __tablename__ = "symptoms"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)

class Disease(Base):
    __tablename__ = "diseases"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(Text)
    treatment = Column(Text)
    symptoms = Column(Text)

    def get_terms(self):
        terms: List[str] = []
        for word in self.name.split():
            terms.append(word)
        
        for word in self.description.split():
            terms.append(word)

        for word in self.treatment.split():
            terms.append(word)

        if self.symptoms:
            for word in self.symptoms.split():
                terms.append(word)

        return terms