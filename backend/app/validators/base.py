from abc import ABC, abstractmethod
from typing import Any, Dict

from backend.app.types import Result


class Validator(ABC):

    @abstractmethod
    def validate(self, data: Any, schema: Dict, path: str, path_json: str, json_map) -> Result:


        """
             Dict:
             {
             "valid": bool,
             "errors": list[{"message", "path", "line"}]
             }
        """
        pass

    @staticmethod
    def get_line(json_map, path_json):
        location = json_map[path_json]
        return location.key_start.line if location.key_start else location.value_start.line