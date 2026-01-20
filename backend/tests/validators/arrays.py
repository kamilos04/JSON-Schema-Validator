import unittest
from unittest.mock import Mock, MagicMock
from backend.app.validators.arrays import ArrayValidator
from backend.app.validators.main import JSONValidator


class TestArrayValidator(unittest.TestCase):
    def setUp(self):
        self.json_validator = Mock(spec=JSONValidator)
        self.json_validator.validate.return_value = {"valid": True, "errors": []}

        self.validator = ArrayValidator(json_validator=self.json_validator)
        self.validator.get_line = MagicMock(return_value=1)
        self.path = "#"
        self.path_json = ""
        self.json_map = {}

    def test_valid_array(self):
        schema = {"minItems" : 1, "maxItems" : 3}
        data = [1, "abc"]
        result = self.validator.validate(data, schema, self.path, self.path_json, self.json_map)
        self.assertTrue(result["valid"])
        self.assertEqual(len(result["errors"]), 0)

    def test_not_an_array(self):
        schema = {"maxItems" : 3}
        data = 10
        result = self.validator.validate(data, schema, self.path, self.path_json, self.json_map)
        self.assertFalse(result["valid"])
        self.assertEqual(len(result["errors"]), 1)
        self.assertIn("Data is not an array", result["errors"][0]["message"])

    def test_items_violation(self):
        schema = {"items": { "type": "string" }}
        data = [7]

        self.json_validator.validate.return_value = {"valid": False, "errors": [{"message": "Mock error"}]}
        
        result = self.validator.validate(data, schema, self.path, self.path_json, self.json_map)
        self.assertFalse(result["valid"])
        self.assertEqual(len(result["errors"]), 1)
        self.assertEqual(result["errors"][0]["message"], "Mock error")

    def test_minItems_violation(self):
        schema = {"minItems" : 3}
        data = [1,"abc"]
        result = self.validator.validate(data, schema, self.path, self.path_json, self.json_map)
        self.assertFalse(result["valid"])
        self.assertEqual(len(result["errors"]), 1)
        self.assertEqual(result["errors"][0]["message"], "Array length (2) is smaller than minItems (3)")
        self.assertEqual(result["errors"][0]["path"], self.path + "/minItems")

    def test_maxItems_violation(self):
        schema = {"maxItems": 3}
        data = [1, "abc", True, 2]
        result = self.validator.validate(data, schema, self.path, self.path_json, self.json_map)
        self.assertFalse(result["valid"])
        self.assertEqual(len(result["errors"]), 1)
        self.assertEqual(result["errors"][0]["message"], "Array length (4) is bigger than maxItems (3)")
        self.assertEqual(result["errors"][0]["path"], self.path + "/maxItems")

    def test_multiple_violations(self):
        schema = {"minItems": 5, "maxItems": 3}
        data = [1, "abc", True, 2]
        result = self.validator.validate(data, schema, self.path, self.path_json, self.json_map)
        self.assertFalse(result["valid"])
        self.assertEqual(len(result["errors"]), 2)

if __name__ == "__main__":
    unittest.main()
