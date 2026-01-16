from typing import Any, Dict, List

from backend.app.types import Result
from backend.app.validators.base import Validator


class LogicValidator(Validator):
    def __init__(self, json_validator):
        self.json_validator = json_validator

    def validate(self, data: Any, schema: Dict, path: str, path_json: str, json_map) -> Result:
        errors: List[Dict] = []

        if "allOf" in schema:
            subschemas = schema["allOf"]

            for subschema in subschemas:
                result = self.json_validator.validate(
                    data=data,
                    schema=subschema,
                    path=path,
                    path_json=path_json,
                    json_map=json_map
                )

                if not result["valid"]:
                    errors.extend(result["errors"])

        if "anyOf" in schema:
            subschemas = schema["anyOf"]
            any_valid = False
            anyof_errors : List[Dict] = []

            for subschema in subschemas:
                result = self.json_validator.validate(
                    data=data,
                    schema=subschema,
                    path=path,
                    path_json=path_json,
                    json_map=json_map                )

                if result["valid"]:
                    any_valid = True
                    break
                else:
                    anyof_errors.extend(result["errors"])

            if not any_valid:
                errors.append({
                    "message": "Data does not match anyOf schemas",
                    "path": path,
                    "line": self.get_line(json_map, path_json, True),
                    "details": anyof_errors
                })

        if "oneOf" in schema:
            subschemas = schema["oneOf"]
            one_valid = False
            more_than_one_valid = False
            oneof_errors: List[Dict] = []

            for subschema in subschemas:
                result = self.json_validator.validate(
                    data=data,
                    schema=subschema,
                    path=path,
                    path_json=path_json,
                    json_map=json_map)

                if result["valid"] and not one_valid:
                    one_valid = True
                elif result["valid"] and one_valid:
                    more_than_one_valid = True
                    break
                else:
                    oneof_errors.extend(result["errors"])

            if not one_valid:
                errors.append({
                    "message": "Data does not match oneOf schemas",
                    "path": path,
                    "line": self.get_line(json_map, path_json, True),
                    "details": oneof_errors
                })
            if more_than_one_valid:
                errors.append({
                    "message": "Data matches more than one oneOf schema",
                    "path": path,
                    "line": self.get_line(json_map, path_json, True),
                })


        if "not" in schema:
            result = self.json_validator.validate(
                data=data,
                schema=schema["not"],
                path=path,
                path_json=path_json,
                json_map=json_map)

            if result["valid"]:
                errors.append({
                    "message": "Data matches not schema",
                    "path": path,
                    "line": self.get_line(json_map, path_json, True),
                })

        if "if" in schema:
            pass

        if "then" in schema:
            pass

        if "else" in schema:
            pass

        return {"valid": not errors, "errors": errors}