import logging

from backend.app.types import Result
from backend.app.validators.main import JSONValidator
from backend.app.validators.types import Validator
from typing import Any, Dict, List


class ObjectValidator(Validator):

    def __init__(self, json_validator):
        self.json_validator = json_validator

    def validate(self, data: Any, schema: Dict, path: str, line: int = 0) -> Result:
        logging.debug("Validating object")
        logging.debug("Data:")
        logging.debug(data)
        logging.debug("Schema:")
        logging.debug(schema)
        logging.debug("\n\n")

        errors: List[Dict] = []


        if not isinstance(data, dict):
            errors.append({"message": "Data is not an object", "path": path, "line": line})
            return {"valid": False, "errors": errors}

        properties = schema.get("properties", {})
        for key, subschema in properties.items():
            if key in data:
                result = self.json_validator.validate(data[key], subschema, path, line)
                errors += result["errors"]


        return {"valid": not errors, "errors": errors}