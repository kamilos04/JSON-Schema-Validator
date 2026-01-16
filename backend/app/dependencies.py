import logging

from backend.app.validators.arrays import ArrayValidator
from backend.app.validators.logic import LogicValidator
from backend.app.validators.main import JSONValidator
from backend.app.validators.numbers import NumberValidator
from backend.app.validators.objects import ObjectValidator
from backend.app.validators.strings import StringValidator
from backend.app.validators.types import TypeValidator

logging.basicConfig(level=logging.DEBUG)

json_validator = JSONValidator(None, None, None, None, None, None)

type_validator = TypeValidator()
object_validator = ObjectValidator(json_validator)
array_validator = ArrayValidator(json_validator)
string_validator = StringValidator()
number_validator = NumberValidator()
logic_validator = LogicValidator(json_validator)

json_validator.type_validator = type_validator
json_validator.object_validator = object_validator
json_validator.array_validator = array_validator
json_validator.string_validator = string_validator
json_validator.number_validator = number_validator
json_validator.logic_validator = logic_validator

