import unittest
from unittest.mock import Mock, MagicMock
from backend.app.validators.logic import LogicValidator
from backend.app.validators.main import JSONValidator

class TestLogicValidator(unittest.TestCase):
    def setUp(self):
        self.json_validator = Mock(spec=JSONValidator)
        self.validator = LogicValidator(json_validator=self.json_validator)
        self.validator.get_line = MagicMock(return_value=1)
        
        self.path = "#"
        self.path_json = ""
        self.json_map = {}
        self.data = "dummy_data"

    def test_allOf_valid(self):
        schema = {"allOf": [{"type": "string"}, {"minLength": 1}]}
        self.json_validator.validate.side_effect = [
            {"valid": True, "errors": []},
            {"valid": True, "errors": []}
        ]

        result = self.validator.validate(self.data, schema, self.path, self.path_json, self.json_map)
        self.assertTrue(result["valid"])
        self.assertEqual(len(result["errors"]), 0)

    def test_allOf_invalid(self):
        schema = {"allOf": [{"type": "string"}, {"minLength": 1}]}
        self.json_validator.validate.side_effect = [
            {"valid": True, "errors": []},
            {"valid": False, "errors": [{"message": "Error 2"}]}
        ]

        result = self.validator.validate(self.data, schema, self.path, self.path_json, self.json_map)
        self.assertFalse(result["valid"])
        self.assertEqual(len(result["errors"]), 1)
        self.assertEqual(result["errors"][0]["message"], "Error 2")

    def test_anyOf_valid(self):
        schema = {"anyOf": [{"type": "string"}, {"type": "integer"}]}
        self.json_validator.validate.side_effect = [
            {"valid": False, "errors": [{"message": "Not a string"}]},
            {"valid": True, "errors": []}
        ]

        result = self.validator.validate(self.data, schema, self.path, self.path_json, self.json_map)
        self.assertTrue(result["valid"])
        self.assertEqual(len(result["errors"]), 0)

    def test_anyOf_invalid(self):
        schema = {"anyOf": [{"type": "string"}, {"type": "integer"}]}
        self.json_validator.validate.side_effect = [
            {"valid": False, "errors": [{"message": "Not a string"}]},
            {"valid": False, "errors": [{"message": "Not an integer"}]}
        ]

        result = self.validator.validate(self.data, schema, self.path, self.path_json, self.json_map)
        self.assertFalse(result["valid"])
        self.assertEqual(len(result["errors"]), 1)
        self.assertIn("Data does not match anyOf schemas", result["errors"][0]["message"])
        self.assertEqual(result["errors"][0]["path"], self.path + "/anyOf")

    def test_oneOf_valid(self):
        schema = {"oneOf": [{"type": "string"}, {"type": "integer"}]}
        self.json_validator.validate.side_effect = [
            {"valid": True, "errors": []},
            {"valid": False, "errors": [{"message": "Not an integer"}]}
        ]

        result = self.validator.validate(self.data, schema, self.path, self.path_json, self.json_map)
        self.assertTrue(result["valid"])
        self.assertEqual(len(result["errors"]), 0)

    def test_oneOf_none_valid(self):
        schema = {"oneOf": [{"type": "string"}, {"type": "integer"}]}
        self.json_validator.validate.side_effect = [
            {"valid": False, "errors": []},
            {"valid": False, "errors": []}
        ]

        result = self.validator.validate(self.data, schema, self.path, self.path_json, self.json_map)
        self.assertFalse(result["valid"])
        self.assertIn("Data does not match oneOf schemas", result["errors"][0]["message"])
        self.assertEqual(result["errors"][0]["path"], self.path + "/oneOf")

    def test_oneOf_multiple_valid(self):
        schema = {"oneOf": [{"type": "string"}, {"minLength": 1}]}
        self.json_validator.validate.side_effect = [
            {"valid": True, "errors": []},
            {"valid": True, "errors": []}
        ]

        result = self.validator.validate(self.data, schema, self.path, self.path_json, self.json_map)
        self.assertFalse(result["valid"])
        self.assertIn("Data matches more than one oneOf schema", result["errors"][0]["message"])
        self.assertEqual(result["errors"][0]["path"], self.path + "/oneOf")

    def test_not_valid(self):
        schema = {"not": {"type": "string"}}
        self.json_validator.validate.return_value = {"valid": False, "errors": [{"message": "Error"}]}

        result = self.validator.validate(self.data, schema, self.path, self.path_json, self.json_map)
        self.assertTrue(result["valid"])
        self.assertEqual(len(result["errors"]), 0)

    def test_not_invalid(self):
        schema = {"not": {"type": "string"}}
        self.json_validator.validate.return_value = {"valid": True, "errors": []}

        result = self.validator.validate(self.data, schema, self.path, self.path_json, self.json_map)
        self.assertFalse(result["valid"])
        self.assertIn("Data matches not schema", result["errors"][0]["message"])
        self.assertEqual(result["errors"][0]["path"], self.path + "/not")

    def test_if_then_valid(self):
        schema = {
            "if": {"const": "a"},
            "then": {"const": "b"}
        }
        self.json_validator.validate.side_effect = [
            {"valid": True, "errors": []},
            {"valid": True, "errors": []}
        ]

        result = self.validator.validate(self.data, schema, self.path, self.path_json, self.json_map)
        self.assertTrue(result["valid"])

    def test_if_then_invalid(self):
        schema = {
            "if": {"const": "a"},
            "then": {"const": "b"}
        }
        self.json_validator.validate.side_effect = [
            {"valid": True, "errors": []},
            {"valid": False, "errors": [{"message": "Then failed"}]}
        ]

        result = self.validator.validate(self.data, schema, self.path, self.path_json, self.json_map)
        self.assertFalse(result["valid"])
        self.assertEqual(result["errors"][0]["message"], "Then failed")

    def test_if_else_valid(self):
        schema = {
            "if": {"const": "a"},
            "else": {"const": "c"}
        }
        self.json_validator.validate.side_effect = [
            {"valid": False, "errors": []},
            {"valid": True, "errors": []}
        ]

        result = self.validator.validate(self.data, schema, self.path, self.path_json, self.json_map)
        self.assertTrue(result["valid"])

    def test_if_else_invalid(self):
        schema = {
            "if": {"const": "a"},
            "else": {"const": "c"}
        }
        self.json_validator.validate.side_effect = [
            {"valid": False, "errors": []},
            {"valid": False, "errors": [{"message": "Else failed"}]}
        ]

        result = self.validator.validate(self.data, schema, self.path, self.path_json, self.json_map)
        self.assertFalse(result["valid"])
        self.assertEqual(result["errors"][0]["message"], "Else failed")

    def test_if_false_no_else(self):
        schema = {"if": {"const": "a"}}
        self.json_validator.validate.return_value = {"valid": False, "errors": []}
        
        result = self.validator.validate(self.data, schema, self.path, self.path_json, self.json_map)
        self.assertTrue(result["valid"])

if __name__ == "__main__":
    unittest.main()