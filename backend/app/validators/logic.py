from typing import Any, Dict, List

from backend.app.validators.base import Validator
from backend.app.validators.main import JSONValidator


class LogicValidator(Validator):
    def __init__(self):
        self.json_validator = JSONValidator()

    def validate(self, data: Any, schema: Dict, path: str, line: int = 0):
        errors: List[Dict] = []

        if "allOf" in schema:
            pass

        if "anyOf" in schema:
            pass

        if "oneOf" in schema:
            pass

        if "not" in schema:
            pass

        if "if" in schema:
            pass


        return {"valid": not errors, "errors": errors}