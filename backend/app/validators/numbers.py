import logging

from backend.app.types import Result
from backend.app.validators.types import Validator
from typing import Any, Dict, List

import math

class NumberValidator(Validator):
    def validate(self, data: Any, schema: Dict, path: str, path_json: str, json_map) -> Result:
        logging.debug("Validating number")
        logging.debug("Data:")
        logging.debug(data)
        logging.debug("Schema:")
        logging.debug(schema)
        logging.debug("Path json:")
        logging.debug(path_json)
        logging.debug("\n\n")

        errors: List[Dict] = []


        if not isinstance(data, (int, float)) or isinstance(data, bool) or not math.isfinite(data):
            errors.append({
                "message": "Data is not a valid finite number",
                "path": path,
                "line": self.get_line(json_map, path_json)
            })
            return {"valid": False, "errors": errors}

        if "minimum" in schema and data < schema["minimum"]:
            errors.append({
                "message": f"Number ({data}) is smaller than minimum ({schema['minimum']})",
                "path": path+"/minimum",
                "line": self.get_line(json_map, path_json)
            })

        if "maximum" in schema and data > schema["maximum"]:
            errors.append({
                "message": f"Number ({data}) is bigger than maximum ({schema['maximum']})",
                "path": path+"/maximum",
                "line": self.get_line(json_map, path_json)
            })

        if "exclusiveMinimum" in schema and data <= schema["exclusiveMinimum"]:
            errors.append({
                "message": f"Number ({data}) is smaller or equal than exclusiveMinimum ({schema['exclusiveMinimum']})",
                "path": path+"/exclusiveMinimum",
                "line": self.get_line(json_map, path_json)
            })

        if "exclusiveMaximum" in schema and data >= schema["exclusiveMaximum"]:
            errors.append({
                "message": f"Number ({data}) is bigger or equal than exclusiveMaximum ({schema['exclusiveMaximum']})",
                "path": path+"/exclusiveMaximum",
                "line": self.get_line(json_map, path_json)
            })

        if "multipleOf" in schema and data % schema["multipleOf"] != 0:
            errors.append({
                "message": f"Number ({data}) is not a multipleOf ({schema['multipleOf']})",
                "path": path+"/multipleOf",
                "line": self.get_line(json_map, path_json)
            })

        return {"valid": not errors, "errors": errors}