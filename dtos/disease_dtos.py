from typing import List, Optional
from pydantic import BaseModel

class DiseaseReadDto(BaseModel):
    id: int
    name: str
    description: str
    treatment: str
    symptoms: Optional[str]

    def get_terms(self):
        terms: List[str] = []
        ignored_words = ["in", "and", "or", "an", "a", "the", "that", "what"]
        for word in self.name.split():
            if word not in ignored_words:
                terms.append(word)

        if self.description:
            for description in self.description.split(","):
                for word in description.split():
                    if word not in ignored_words:
                        terms.append(word)

        if self.treatment:
            for treatment in self.treatment.split(","):
                for word in treatment.split():
                    if word not in ignored_words:
                        terms.append(word)

        if self.symptoms:
            for symptom in self.symptoms.split(","):
                for word in symptom.split():
                    if word not in ignored_words:
                        terms.append(word)

        return terms

    class Config:
        orm_mode = True


class DiseaseWriteDto(BaseModel):
    name: str
    description: str
    treatment: str
    symptoms: Optional[str]

    class Config:
        orm_mode = True