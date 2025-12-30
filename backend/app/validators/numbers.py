import logging

from backend.app.types import Result
from backend.app.validators.types import Validator
from typing import Any, Dict, List


class NumberValidator(Validator):
    def validate(self, data: Any, schema: Dict, path: str, line: int = 0) -> Result:
        logging.debug("Validating number")
        logging.debug("Data:")
        logging.debug(data)
        logging.debug("Schema:")
        logging.debug(schema)
        logging.debug("\n\n")

        errors: List[Dict] = []


        if not isinstance(data, (int, float)) or isinstance(data, bool):
            errors.append({"message": "Data is not a number", "path": path, "line": line})
            return {"valid": False, "errors": errors}

        if "minimum" in schema and data < schema["minimum"]:
            errors.append({
                "message": f"Number is smaller ({data}) than minimum ({schema['minimum']})",
                "path": path,
                "line": line
            })

        if "maximum" in schema and data > schema["maximum"]:
            errors.append({
                "message": f"Number is bigger ({data}) than maximum ({schema['maximum']})",
                "path": path,
                "line": line
            })

        if "exclusiveMinimum" in schema and data <= schema["exclusiveMinimum"]:
            errors.append({
                "message": f"Number is smaller or equal ({data}) than exclusiveMinimum ({schema['exclusiveMinimum']})",
                "path": path,
                "line": line
            })

        if "exclusiveMaximum" in schema and data >= schema["exclusiveMaximum"]:
            errors.append({
                "message": f"Number is bigger or equal ({data}) than exclusiveMaximum ({schema['exclusiveMaximum']})",
                "path": path,
                "line": line
            })

        if "multipleOf" in schema and data % schema["multipleOf"] != 0:
            errors.append({
                "message": f"Number is not a multiple of ({schema['multipleOf']})",
                "path": path,
                "line": line
            })

        return {"valid": not errors, "errors": errors}