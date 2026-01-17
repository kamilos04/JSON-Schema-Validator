import json
from backend.app.dependencies import json_validator
from json_source_map import calculate

# Test
schema = """
{
    "type": "object",
    "required": ["age", "can_vote"],
    "properties": {
        "age": {"type": "integer"},
        "can_vote": {"type": "boolean"}
    },
    "if": {
        "type": "object",
        "properties": {
            "age": {"type": "integer", "minimum": 18}
        }
    },
    "then": {
        "type": "object",
        "properties": {
            "can_vote": {"type": "boolean", "const": true}
        }
    },
    "else": {
        "type": "object",
        "properties": {
            "can_vote": {"type": "boolean", "const": false}
        }
    }
}
"""

json_data = """
{
    "age": 20,
    "can_vote": false
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

