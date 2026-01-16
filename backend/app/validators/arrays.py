import logging

from backend.app.types import Result
from backend.app.validators.types import Validator
from typing import Any, Dict, List


class ArrayValidator(Validator):
    def __init__(self, json_validator):
        self.json_validator = json_validator

    def validate(self, data: Any, schema: Dict, path: str, path_json: str, json_map) -> Result:
        logging.debug("Validating array")
        logging.debug("Data:")
        logging.debug(data)
        logging.debug("Schema:")
        logging.debug(schema)
        logging.debug("Path json:")
        logging.debug(path_json)
        logging.debug("\n\n")

        errors: List[Dict] = []

        if not isinstance(data, list):
            errors.append({
                "message": "Data is not an array",
                "path": path,
                "line": self.get_line(json_map, path_json)
            })
            return {"valid": False, "errors": errors}

        if "items" in schema:
            item_schema = schema["items"]

            for index, item in enumerate(data):
                result = self.json_validator.validate(data=item, schema=item_schema, path=path+"/items", path_json=path_json+f"/{index}", json_map=json_map)
                if not result["valid"]:
                    errors.extend(result["errors"])

        if "minItems" in schema and len(data) < schema["minItems"]:
            errors.append({
                "message": f"Array length ({len(data)}) is smaller than minItems ({schema['minItems']})",
                "path": path+"/minItems",
                "line": self.get_line(json_map, path_json)
            })

        if "maxItems" in schema and len(data) > schema["maxItems"]:
            errors.append({
                "message": f"Array length ({len(data)}) is bigger than maxItems ({schema['maxItems']})",
                "path": path+"/maxItems",
                "line": self.get_line(json_map, path_json)
            })

        return {"valid": not errors, "errors": errors}