from backend.app.dependencies import json_validator

# Test
schema = {
  "type": "object",
  "required": ["name", "age"],
  "minProperties": 3,
  "maxProperties": 3,
  "properties": {
    "name": { "type": "string", "minLength": 4, "maxLength": 7 },
    "age": { "type": "integer" }
  }
}

json_data = {
  "name": 'Ka',
  "age": 21,
  "test": 1,
  "test2": 2
}



json_result = json_validator.validate(json_data, schema, "")
print(json_result)

