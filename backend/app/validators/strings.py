from backend.app.validators.types import Validator
from typing import Any, Dict, List
import re


class StringValidator(Validator):
    def validate(self, data: Any, schema: Dict, path: str, line: int = 0):
        errors: List[Dict] = []

        if not isinstance(data, str):
            errors.append({"message": "Data is not a string", "path": path, "line": line})
            return {"valid": False, "errors": errors}

        if "minLength" in schema and len(data) < schema["minLength"]:
            errors.append({"message": f"String length {len(data)} < minLength {schema['minLength']}", "path": path, "line": line})
        if "maxLength" in schema and len(data) > schema["maxLength"]:
            errors.append(
                {"message": f"String length {len(data)} > maxLength {schema['maxLength']}", "path": path, "line": line})
        if "pattern" in schema and not re.match(schema["pattern"], data):
            errors.append(
                {"message": f"String {data} does not match pattern {schema['pattern']}", "path": path, "line": line})

        return {"valid": not errors, "errors": errors}