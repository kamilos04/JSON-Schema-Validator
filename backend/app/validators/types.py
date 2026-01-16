import logging
import math
from typing import Any, Dict, List

from backend.app.types import Result
from backend.app.validators.base import Validator


class TypeValidator(Validator):

    @staticmethod
    def matches_type(value: Any, schema_type: str) -> bool:
        if schema_type == "string":
            return isinstance(value, str)

        if schema_type == "number":
            return (isinstance(value, (int, float))
                    and not isinstance(value, bool)
                    and math.isfinite(value)
            )

        if schema_type == "integer":
            return isinstance(value, int) and not isinstance(value, bool)

        if schema_type == "object":
            return isinstance(value, dict)

        if schema_type == "array":
            return isinstance(value, list)

        if schema_type == "boolean":
            return isinstance(value, bool)

        if schema_type == "null":
            return value is None

        return False

    def validate(self, data: Any, schema: Dict, path: str, line: int = 0) -> Result:
        logging.debug("Validating type")
        logging.debug("Data:")
        logging.debug(data)
        logging.debug("Schema:")
        logging.debug(schema)
        logging.debug("\n\n")

        errors: List[Dict] = []

        if "type" in schema:
            if isinstance(schema["type"], list):
                allowed_types = schema["type"]
            else:
                allowed_types = [schema["type"]]
            if not any(self.matches_type(data, t) for t in allowed_types):
                errors.append({
                    "message": "Data does not match any of the allowed types",
                    "path": path,
                    "line": line
                })
        if "enum" in schema:
            if not any(item == data and type(item) is type(data) for item in schema["enum"]):
                errors.append({
                    "message": "Data does not match any of the enum values",
                    "path": path,
                    "line": line
                })

        if "const" in schema:
            if not (data == schema["const"] and type(data) is type(schema["const"])):
                errors.append({
                    "message": "Data does not match the const value",
                    "path": path,
                    "line": line
                })
                
        return {"valid": not errors, "errors": errors}