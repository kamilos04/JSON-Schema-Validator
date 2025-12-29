from backend.app.dependencies import json_validator



# Test
schema = {
  "type": "object",
  "required": ["name", "age"],
  "properties": {
    "name": { "type": "string", "minLength": 5, "maxLength": 7 },
    "age": { "type": "integer" }
  }
}

json = {
  "name": 'Kamil',
  "age": 21
}


json_result = json_validator.validate(json, schema, "")
print(json_result)

