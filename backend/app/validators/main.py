from typing import Any, Dict, List

from backend.app.types import Result
from backend.app.validators.base import Validator
from json_source_map import calculate


class JSONValidator(Validator):

    def __init__(self, type_validator, object_validator, array_validator, string_validator, number_validator, logic_validator):
        self.type_validator = type_validator
        self.object_validator = object_validator
        self.array_validator = array_validator
        self.string_validator = string_validator
        self.number_validator = number_validator
        self.logic_validator = logic_validator


    def validate(self, data: Any, schema: Dict, path: str, path_json: str, json_map) -> Result:

        type_result = self.type_validator.validate(data, schema, path, path_json, json_map)
        if not type_result["valid"]:
            return type_result

        schema_type = schema.get("type")
        if schema_type == "object":
            base_result = self.object_validator.validate(data, schema, path, path_json, json_map)
        elif schema_type == "array":
            base_result = self.array_validator.validate(data, schema, path, path_json, json_map)
        elif schema_type == "string":
            base_result = self.string_validator.validate(data, schema, path, path_json, json_map)
        elif schema_type in ["integer", "number"]:
            base_result = self.number_validator.validate(data, schema, path, path_json, json_map)
        else:
            base_result = {"valid": True, "errors": []}

        logic_result = self.logic_validator.validate(data, schema, path, path_json, json_map)

        errors: List[Dict] = base_result["errors"] + logic_result["errors"]

        return {"valid": not errors, "errors": errors}