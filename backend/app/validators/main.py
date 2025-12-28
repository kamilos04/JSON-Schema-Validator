from typing import Any, Dict, List

from backend.app.validators.arrays import ArrayValidator
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



    def validate(self, data: Any, schema: Dict, path: str, line: int = 0):
        errors: List[Dict] = []



        return {"valid": not errors, "errors": errors}