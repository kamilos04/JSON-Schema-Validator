from abc import ABC, abstractmethod
from typing import Any, Dict

from backend.app.types import Result


class Validator(ABC):

    @abstractmethod
    def validate(self, data: Any, schema: Dict, path: str, line: int = 0) -> Result:


        """
             Dict:
             {
             "valid": bool,
             "errors": list[{"message", "path", "line"}]
             }
        """
        pass