import logging

from backend.app.types import Result
from backend.app.validators.types import Validator
from typing import Any, Dict, List
import re


class StringValidator(Validator):
    def validate(self, data: Any, schema: Dict, path: str, path_json: str, json_map)  -> Result:
        logging.debug("Validating string")
        logging.debug("Data:")
        logging.debug(data)
        logging.debug("Schema:")
        logging.debug(schema)
        logging.debug("Path json:")
        logging.debug(path_json)
        logging.debug("\n\n")

        errors: List[Dict] = []

        if not isinstance(data, str):
            errors.append({
                "message": "Data is not a string",
                "path": path,
                "line": self.get_line(json_map, path_json, True)
            })
            logging.info("\nData is not a string\n")
            return {"valid": False, "errors": errors}

        if "minLength" in schema and len(data) < schema["minLength"]:
            errors.append({
                "message": f"String length ({len(data)}) < minLength ({schema['minLength']})",
                "path": path+"/minLength",
                "line": self.get_line(json_map, path_json, True)
            })
            logging.info(f"\nString length ({len(data)}) < minLength ({schema['minLength']})\n")

        if "maxLength" in schema and len(data) > schema["maxLength"]:
            errors.append({
                "message": f"String length ({len(data)}) > maxLength ({schema['maxLength']})",
                "path": path+"/maxLength",
                "line": self.get_line(json_map, path_json, True)
            })
            logging.info(f"\nString length ({len(data)}) > maxLength ({schema['maxLength']})\n")

        if "pattern" in schema and not re.match(schema["pattern"], data):
            errors.append({
                "message": f"String '{data}' does not match pattern {schema['pattern']}",
                "path": path+"/pattern",
                "line": self.get_line(json_map, path_json, True)
            })
            logging.info(f"\nString '{data}' does not match pattern {schema['pattern']}\n")

        return {"valid": not errors, "errors": errors}