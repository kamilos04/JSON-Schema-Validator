from abc import ABC, abstractmethod
from typing import Any, Dict

class Validator(ABC):

    @abstractmethod
    def validate(self, data: Any, schema: Dict, path: str, line: int = 0) -> Dict:


        """
             Dict:
             {
             "valid": bool,
             "errors": list[{"message", "path", "line"}]
             }
        """
        pass