from typing import Any, Callable, List, Optional, Tuple, Union
from backend.app.validators.base import Validator

class ValidatorDispatcher:
    def __init__(self):
        self._strategies: List[Tuple[Callable[[Any], bool], Union[Validator, Callable[[], Validator]]]] = []

    def register(self, condition: Callable[[Any], bool], validator: Union[Validator, Callable[[], Validator]]):
        self._strategies.append((condition, validator))

    def get_validator(self, data: Any) -> Optional[Validator]:
        for condition, validator in self._strategies:
            if condition(data):
                if isinstance(validator, Validator):
                    return validator
                elif callable(validator):
                    return validator()
        return None