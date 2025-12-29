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


    def validate(self, data: Any, schema: Dict, path: str, line: int = 0):
        errors: List[Dict] = []



        logic_result = self.logic_validator.validate(data, schema, path, line)

        # errors = base_result["errors"] + logic_result["errors"]

        return {"valid": not errors, "errors": errors}