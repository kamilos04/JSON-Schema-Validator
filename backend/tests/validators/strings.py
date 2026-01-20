import unittest
from unittest.mock import MagicMock
from backend.app.validators.strings import StringValidator

class TestStringValidator(unittest.TestCase):
    def setUp(self):
        self.validator = StringValidator()
        self.validator.get_line = MagicMock(return_value=1)
        self.path = "#"
        self.path_json = ""
        self.json_map = {}

    def test_valid_string(self):
        schema = {"minLength": 2, "maxLength": 10}
        data = "hello"
        result = self.validator.validate(data, schema, self.path, self.path_json, self.json_map)
        self.assertTrue(result["valid"])
        self.assertEqual(len(result["errors"]), 0)

    def test_not_a_string(self):
        schema = {"minLength": 2}
        data = 123
        result = self.validator.validate(data, schema, self.path, self.path_json, self.json_map)
        self.assertFalse(result["valid"])
        self.assertEqual(len(result["errors"]), 1)
        self.assertIn("Data is not a string", result["errors"][0]["message"])

    def test_min_length_violation(self):
        schema = {"minLength": 5}
        data = "abc"
        result = self.validator.validate(data, schema, self.path, self.path_json, self.json_map)
        self.assertFalse(result["valid"])
        self.assertEqual(len(result["errors"]), 1)
        self.assertEqual(result["errors"][0]["message"], "String length (3) < minLength (5)")
        self.assertEqual(result["errors"][0]["path"], self.path + "/minLength")

    def test_max_length_violation(self):
        schema = {"maxLength": 3}
        data = "abcdef"
        result = self.validator.validate(data, schema, self.path, self.path_json, self.json_map)
        self.assertFalse(result["valid"])
        self.assertEqual(len(result["errors"]), 1)
        self.assertEqual(result["errors"][0]["message"], "String length (6) > maxLength (3)")
        self.assertEqual(result["errors"][0]["path"], self.path + "/maxLength")

    def test_pattern_match_valid(self):
        schema = {"pattern": r"^[a-z]+$"}
        data = "abc"
        result = self.validator.validate(data, schema, self.path, self.path_json, self.json_map)
        self.assertTrue(result["valid"])

    def test_pattern_match_invalid(self):
        schema = {"pattern": r"^[a-z]+$"}
        data = "abc123"
        result = self.validator.validate(data, schema, self.path, self.path_json, self.json_map)
        self.assertFalse(result["valid"])
        self.assertEqual(len(result["errors"]), 1)
        self.assertIn("does not match pattern", result["errors"][0]["message"])
        self.assertEqual(result["errors"][0]["path"], self.path + "/pattern")

    def test_multiple_violations(self):
        schema = {"minLength": 5, "maxLength": 10, "pattern": r"^[A-Z]+$"}
        data = "abc"
        result = self.validator.validate(data, schema, self.path, self.path_json, self.json_map)
        self.assertFalse(result["valid"])
        self.assertEqual(len(result["errors"]), 2)
        
        messages = [e["message"] for e in result["errors"]]
        self.assertIn("String length (3) < minLength (5)", messages)
        self.assertTrue(any("does not match pattern" in m for m in messages))

if __name__ == "__main__":
    unittest.main()
