import logging

from backend.app.types import Result
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
            errors.append({
                "message": "Data is not an object",
                "path": path,
                "line": line
            })
            return {"valid": False, "errors": errors}

        if "minProperties" in schema and len(data) < schema["minProperties"]:
            errors.append({
                "message": f"Object has fewer properties ({len(data)}) than minProperties ({schema['minProperties']})",
                "path": path+"/minProperties",
                "line": line
            })
        if "maxProperties" in schema and len(data) > schema["maxProperties"]:
            errors.append({
                "message": f"Object has more properties ({len(data)}) than maxProperties ({schema['maxProperties']})",
                "path": path+"/maxProperties",
                "line": line
            })

        for key in schema.get("required", []):
            if key not in data:
                errors.append({
                    "message": f"Missing required property: {key}",
                    "path": path+'/required',
                    "line": line
                })

        properties = schema.get("properties", {})
        for key, subschema in properties.items():
            if key in data:
                result = self.json_validator.validate(data[key], subschema, path+'/properties', line)
                errors += result["errors"]


        return {"valid": not errors, "errors": errors}