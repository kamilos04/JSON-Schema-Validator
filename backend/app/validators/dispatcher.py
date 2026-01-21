from typing import Any, Callable, List, Optional, Tuple
from backend.app.validators.base import Validator

class ValidatorDispatcher:
    def __init__(self):
        self._strategies: List[Tuple[Callable[[Any], bool], Validator]] = []

    def register(self, condition: Callable[[Any], bool], validator: Validator):
        self._strategies.append((condition, validator))

    def get_validator(self, data: Any) -> Optional[Validator]:
        for condition, validator in self._strategies:
            if condition(data):
                return validator
        return None