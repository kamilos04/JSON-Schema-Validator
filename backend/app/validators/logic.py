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

            for index, subschema in enumerate(subschemas):
                result = self.json_validator.validate(
                    data=data,
                    schema=subschema,
                    path=path + f"/allOf/{index}",
                    path_json=path_json,
                    json_map=json_map
                )

                if not result["valid"]:
                    errors.extend(result["errors"])

        if "anyOf" in schema:
            subschemas = schema["anyOf"]
            any_valid = False
            anyof_errors : List[Dict] = []

            for index, subschema in enumerate(subschemas):
                result = self.json_validator.validate(
                    data=data,
                    schema=subschema,
                    path=path + f"/anyOf/{index}",
                    path_json=path_json,
                    json_map=json_map)

                if result["valid"]:
                    any_valid = True
                    break
                else:
                    anyof_errors.extend(result["errors"])

            if not any_valid:
                errors.append({
                    "message": "Data does not match anyOf schemas",
                    "path": path + "/anyOf",
                    "line": self.get_line(json_map, path_json),
                    "details": anyof_errors
                })

        if "oneOf" in schema:
            subschemas = schema["oneOf"]
            one_valid = False
            more_than_one_valid = False
            oneof_errors: List[Dict] = []

            for index, subschema in enumerate(subschemas):
                result = self.json_validator.validate(
                    data=data,
                    schema=subschema,
                    path=path + f"/oneOf/{index}",
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
                    "path": path + "/oneOf",
                    "line": self.get_line(json_map, path_json),
                    "details": oneof_errors
                })
            if more_than_one_valid:
                errors.append({
                    "message": "Data matches more than one oneOf schema",
                    "path": path + "/oneOf",
                    "line": self.get_line(json_map, path_json),
                })


        if "not" in schema:
            result = self.json_validator.validate(
                data=data,
                schema=schema["not"],
                path=path + "/not",
                path_json=path_json,
                json_map=json_map)

            if result["valid"]:
                errors.append({
                    "message": "Data matches not schema",
                    "path": path + "/not",
                    "line": self.get_line(json_map, path_json),
                })

        if "if" in schema:
            if_schema = schema["if"]
            then_schema = schema.get("then")
            else_schema = schema.get("else")

            if_result = self.json_validator.validate(
                data = data,
                schema=if_schema,
                path=path + "/if",
                path_json=path_json,
                json_map=json_map)

            if if_result["valid"] and then_schema:
                then_result = self.json_validator.validate(
                    data = data,
                    schema=then_schema,
                    path=path + "/then",
                    path_json=path_json,
                    json_map=json_map)
                if not then_result["valid"]:
                    errors.extend(then_result["errors"])
            elif not if_result["valid"] and else_schema:
                else_result = self.json_validator.validate(
                    data = data,
                    schema=else_schema,
                    path=path + "/else",
                    path_json=path_json,
                    json_map=json_map)
                if not else_result["valid"]:
                    errors.extend(else_result["errors"])

        return {"valid": not errors, "errors": errors}