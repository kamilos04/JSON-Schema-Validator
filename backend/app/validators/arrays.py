from backend.app.validators.types import Validator
from typing import Any, Dict, List


class ArrayValidator(Validator):
    def validate(self, data: Any, schema: Dict, path: str, line: int = 0):
        errors: List[Dict] = []



        return {"valid": not errors, "errors": errors}