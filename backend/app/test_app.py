import json
from backend.app.dependencies import json_validator
from json_source_map import calculate

# Test
schema = """
{
    "oneOf": [
        {
            "type": "object",
            "properties": {
                "name": {"type": "string", "minLength": 4}
            }
        },
        {
            "type": "object",
            "properties": {
                "age": {"type": "integer", "minimum": 18}
            }
        }
    ]
}
"""

json_data = """
{
  "name": "Ka",
  "age": 11

}
"""

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

json_dict = json.loads(json_data)
schema_dict = json.loads(schema)
json_map = calculate(json_data)
print(json_validator.validate(json_dict, schema_dict, "#", "", json_map))

