from typing import Any, Dict, List

from backend.app.types import Result
from backend.app.validators.base import Validator
from backend.app.validators.dispatcher import ValidatorDispatcher


class JSONValidator(Validator):

    def __init__(self, type_validator, object_validator, array_validator, string_validator, number_validator, logic_validator):
        self.type_validator = type_validator
        self.logic_validator = logic_validator

        self.dispatcher = ValidatorDispatcher()
        self.dispatcher.register(lambda d: isinstance(d, dict), object_validator)
        self.dispatcher.register(lambda d: isinstance(d, list), array_validator)
        self.dispatcher.register(lambda d: isinstance(d, str), string_validator)
        self.dispatcher.register(
            lambda d: isinstance(d, (int, float)) and not isinstance(d, bool), 
            number_validator
        )


    def validate(self, data: Any, schema: Dict, path: str, path_json: str, json_map) -> Result:

        type_result = self.type_validator.validate(data, schema, path, path_json, json_map)
        if not type_result["valid"]:
            return type_result

        base_result = {"valid": True, "errors": []}

        strategy_validator = self.dispatcher.get_validator(data)
        if strategy_validator:
            base_result = strategy_validator.validate(data, schema, path, path_json, json_map)

        logic_result = self.logic_validator.validate(data, schema, path, path_json, json_map)

        errors: List[Dict] = base_result["errors"] + logic_result["errors"]

        return {"valid": not errors, "errors": errors}