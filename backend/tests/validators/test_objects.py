import unittest
from unittest.mock import Mock, MagicMock
from backend.app.validators.objects import ObjectValidator
from backend.app.validators.main import JSONValidator

class TestObjectValidator(unittest.TestCase):
    def setUp(self):
        self.json_validator = Mock(spec=JSONValidator)
        self.json_validator.validate.return_value = {"valid": True, "errors": []}

        self.validator = ObjectValidator(json_validator=self.json_validator)
        self.validator.get_line = MagicMock(return_value=1)
        
        self.path = "#"
        self.path_json = ""
        self.json_map = {}

    def test_valid_object(self):
        schema = {"minProperties": 1}
        data = {"key": "value"}
        result = self.validator.validate(data, schema, self.path, self.path_json, self.json_map)
        self.assertTrue(result["valid"])
        self.assertEqual(len(result["errors"]), 0)

    def test_not_an_object(self):
        schema = {}
        data = ["not", "an", "object"]
        result = self.validator.validate(data, schema, self.path, self.path_json, self.json_map)
        self.assertFalse(result["valid"])
        self.assertEqual(len(result["errors"]), 1)
        self.assertIn("Data is not an object", result["errors"][0]["message"])

    def test_min_properties_violation(self):
        schema = {"minProperties": 2}
        data = {"a": 1}
        result = self.validator.validate(data, schema, self.path, self.path_json, self.json_map)
        self.assertFalse(result["valid"])
        self.assertEqual(len(result["errors"]), 1)
        self.assertIn("Object has fewer properties (1) than minProperties (2)", result["errors"][0]["message"])
        self.assertEqual(result["errors"][0]["path"], self.path + "/minProperties")

    def test_max_properties_violation(self):
        schema = {"maxProperties": 1}
        data = {"a": 1, "b": 2}
        result = self.validator.validate(data, schema, self.path, self.path_json, self.json_map)
        self.assertFalse(result["valid"])
        self.assertEqual(len(result["errors"]), 1)
        self.assertIn("Object has more properties (2) than maxProperties (1)", result["errors"][0]["message"])
        self.assertEqual(result["errors"][0]["path"], self.path + "/maxProperties")

    def test_required_violation(self):
        schema = {"required": ["name", "age"]}
        data = {"name": "Kamil"}
        result = self.validator.validate(data, schema, self.path, self.path_json, self.json_map)
        self.assertFalse(result["valid"])
        self.assertEqual(len(result["errors"]), 1)
        self.assertIn("Missing required property: age", result["errors"][0]["message"])
        self.assertEqual(result["errors"][0]["path"], self.path + "/required")

    def test_properties_delegation_failure(self):
        schema = {
            "properties": {
                "age": {"type": "integer"}
            }
        }
        data = {"age": "invalid"}

        self.json_validator.validate.return_value = {
            "valid": False, 
            "errors": [{"message": "Type mismatch", "path": "#/properties/age"}]
        }

        result = self.validator.validate(data, schema, self.path, self.path_json, self.json_map)
        self.assertFalse(result["valid"])
        self.assertEqual(len(result["errors"]), 1)
        self.assertEqual(result["errors"][0]["message"], "Type mismatch")

        self.json_validator.validate.assert_called()

    def test_additional_properties_false(self):
        schema = {
            "properties": {"a": {}},
            "additionalProperties": False
        }
        data = {"a": 1, "b": 2}
        result = self.validator.validate(data, schema, self.path, self.path_json, self.json_map)
        self.assertFalse(result["valid"])
        self.assertEqual(len(result["errors"]), 1)
        self.assertIn("Additional property 'b' is not allowed", result["errors"][0]["message"])
        self.assertEqual(result["errors"][0]["path"], self.path + "/additionalProperties")

    def test_additional_properties_schema(self):
        schema = {
            "additionalProperties": {"type": "string"}
        }
        data = {"extra": 123}

        self.json_validator.validate.return_value = {"valid": False, "errors": [{"message": "Not a string"}]}

        result = self.validator.validate(data, schema, self.path, self.path_json, self.json_map)
        self.assertFalse(result["valid"])
        self.assertEqual(len(result["errors"]), 1)
        self.assertEqual(result["errors"][0]["message"], "Not a string")

if __name__ == "__main__":
    unittest.main()