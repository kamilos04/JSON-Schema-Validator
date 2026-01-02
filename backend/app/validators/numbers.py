import logging

from backend.app.types import Result
from backend.app.validators.types import Validator
from typing import Any, Dict, List


class NumberValidator(Validator):
    def validate(self, data: Any, schema: Dict, path: str, line: int = 0) -> Result:
        logging.debug("Validating number")
        logging.debug("Data:")
        logging.debug(data)
        logging.debug("Schema:")
        logging.debug(schema)
        logging.debug("\n\n")

        errors: List[Dict] = []



        return {"valid": not errors, "errors": errors}