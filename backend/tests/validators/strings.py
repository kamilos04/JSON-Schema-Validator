import unittest
from backend.app.validators.strings import StringValidator

class TestStringValidator(unittest.TestCase):
    def setUp(self):
        self.validator = StringValidator()
        self.path = "root"
        self.line = 1

    def test_valid_string(self):
        schema = {"minLength": 2, "maxLength": 10}
        data = "hello"
        result = self.validator.validate(data, schema, self.path, self.line)
        self.assertTrue(result["valid"])
        self.assertEqual(len(result["errors"]), 0)

    def test_not_a_string(self):
        schema = {"minLength": 2}
        data = 123
        result = self.validator.validate(data, schema, self.path, self.line)
        self.assertFalse(result["valid"])
        self.assertEqual(len(result["errors"]), 1)
        self.assertIn("Data is not a string", result["errors"][0]["message"])

    def test_min_length_violation(self):
        schema = {"minLength": 5}
        data = "abc"
        result = self.validator.validate(data, schema, self.path, self.line)
        self.assertFalse(result["valid"])
        self.assertEqual(len(result["errors"]), 1)
        self.assertIn("String length 3 < minLength 5", result["errors"][0]["message"])

    def test_max_length_violation(self):
        schema = {"maxLength": 3}
        data = "abcdef"
        result = self.validator.validate(data, schema, self.path, self.line)
        self.assertFalse(result["valid"])
        self.assertEqual(len(result["errors"]), 1)
        self.assertIn("String length 6 > maxLength 3", result["errors"][0]["message"])

    def test_pattern_match(self):
        schema = {"pattern": r"^[a-z]+$"}
        data = "abc123"
        result = self.validator.validate(data, schema, self.path, self.line)
        self.assertFalse(result["valid"])
        self.assertEqual(len(result["errors"]), 1)
        self.assertIn("does not match pattern", result["errors"][0]["message"])

    def test_multiple_violations(self):
        schema = {"minLength": 5, "maxLength": 10, "pattern": r"^[A-Z]+$"}
        data = "abc"
        result = self.validator.validate(data, schema, self.path, self.line)
        self.assertFalse(result["valid"])
        self.assertEqual(len(result["errors"]), 2)

if __name__ == "__main__":
    unittest.main()
