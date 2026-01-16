import logging

from backend.app.types import Result
from backend.app.validators.types import Validator
from typing import Any, Dict, List


class ArrayValidator(Validator):
    def __init__(self, json_validator):
        self.json_validator = json_validator


    def validate(self, data: Any, schema: Dict, path: str, line: int = 0) -> Result:
        logging.debug("Validating array")
        logging.debug("Data:")
        logging.debug(data)
        logging.debug("Schema:")
        logging.debug(schema)
        logging.debug("\n\n")

        errors: List[Dict] = []

        if not isinstance(data, list):
            errors.append({"message": "Data is not an array", "path": path, "line": line})
            return {"valid": False, "errors": errors}

        if "items" in schema:
            item_schema = schema["items"]

            for index, item in enumerate(data):
                result = self.json_validator.validate(data=item, schema=item_schema, path=f"{path}[{index}]", line=line)
                if not result["valid"]:
                    errors.extend(result["errors"])

        if "minItems" in schema and len(data) < schema["minItems"]:
            errors.append({
                "message": f"Array length ({len(data)}) is smaller than minItems ({schema['minItems']})",
                "path": path,
                "line": line
            })

        if "maxItems" in schema and len(data) > schema["maxItems"]:
            errors.append({
                "message": f"Array length ({len(data)}) is bigger than maxItems ({schema['maxItems']})",
                "path": path,
                "line": line
            })

        return {"valid": not errors, "errors": errors}