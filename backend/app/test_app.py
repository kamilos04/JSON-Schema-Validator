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
  "name": "Ka",
  "age": 21,
  "test": 1,
  "test2": 2
}

# schema = {
#     "type": "object",
#     "required": ["name", "age", "address"],
#     "properties": {
#         "name": { "type": "string", "minLength": 3, "maxLength": 10 },
#         "age": { "type": "integer" },
#         "address": {
#             "type": "object",
#             "required": ["street", "city"],
#             "properties": {
#                 "street": { "type": "string", "minLength": 5 },
#                 "city": { "type": "string", "minLength": 2 }
#             }
#         }
#     }
# }
#
# json_data = {
#     "name": "Kamil",
#     "age": 25,
#     "address": {
#         "street": 12,
#         "city": "Warszawa"
#     }
# }


json_result = json_validator.validate(json_data, schema, "")
print(json_result)

