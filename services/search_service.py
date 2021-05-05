from typing import Dict, Tuple

from fastapi.param_functions import Depends


class Index:
    def __init__(self) -> None:
        self.weight_function: Dict[Tuple[str, int], float] = {}
        self.system_terms: Dict[str, int] = {}
        self.total_documents: int = 0

    def __call__(self):
        return self

index = Index()

class SerchService:

    # Use Dependency Injection here on services that this might depend
    def __init__(self, indx: Index = Depends(index)):
        self.index = indx