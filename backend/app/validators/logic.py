from typing import Any, Dict, List

from backend.app.types import Result
from backend.app.validators.base import Validator


class LogicValidator(Validator):
    def __init__(self, json_validator):
        self.json_validator = json_validator

    def validate(self, data: Any, schema: Dict, path: str, line: int = 0) -> Result:
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