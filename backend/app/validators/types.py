import logging
from typing import Any, Dict, List

from backend.app.types import Result
from backend.app.validators.base import Validator


class TypeValidator(Validator):

    def validate(self, data: Any, schema: Dict, path: str, path_json: str, json_map) -> Result:
        logging.debug("Validating type")
        logging.debug("Data:")
        logging.debug(data)
        logging.debug("Schema:")
        logging.debug(schema)
        logging.debug("Path json:")
        logging.debug(path_json)
        logging.debug("\n\n")

        errors: List[Dict] = []



        return {"valid": not errors, "errors": errors}