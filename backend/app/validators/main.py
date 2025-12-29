from typing import Any, Dict, List

from backend.app.validators.arrays import ArrayValidator
from backend.app.validators.logic import LogicValidator
from backend.app.validators.numbers import NumberValidator
from backend.app.validators.objects import ObjectValidator
from backend.app.validators.strings import StringValidator
from backend.app.validators.types import TypeValidator


class JSONValidator:

    def __init__(self):
        self.type_validator = TypeValidator()
        self.object_validator = ObjectValidator()
        self.array_validator = ArrayValidator()
        self.string_validator = StringValidator()
        self.number_validator = NumberValidator()
        self.logic_validator = LogicValidator()


    def validate(self, data: Any, schema: Dict, path: str, line: int = 0) -> Dict:
        type_result = self.type_validator.validate(data, schema, path, line)
        if not type_result["valid"]:
            return type_result

        schema_type = schema.get("type")
        if schema_type == "object":
            base_result = self.object_validator.validate(data, schema, path, line)
        elif schema_type == "array":
            base_result = self.array_validator.validate(data, schema, path, line)
        elif schema_type == "string":
            base_result = self.string_validator.validate(data, schema, path, line)
        elif schema_type == "number":
            base_result = self.number_validator.validate(data, schema, path, line)
        else:
            base_result = {"valid": True, "errors": []}

        logic_result = self.logic_validator.validate(data, schema, path, line)

        errors = base_result["errors"] + logic_result["errors"]

        return {"valid": not errors, "errors": errors}