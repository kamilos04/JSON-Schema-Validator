import unittest
from backend.app.validators.types import TypeValidator

class TestTypeValidator(unittest.TestCase):
    def setUp(self):
        self.validator = TypeValidator()
        self.path = "root"
        self.line = 1

    def test_valid_type(self):
        schema = {"type": "integer"}
        data = 10
        result = self.validator.validate(data, schema, self.path, self.line)
        self.assertTrue(result["valid"])
        self.assertEqual(len(result["errors"]), 0)

    def test_type_violation(self):
        schema = {"type": ["integer","string"]}
        data = 1.2
        result = self.validator.validate(data, schema, self.path, self.line)
        self.assertFalse(result["valid"])
        self.assertEqual(len(result["errors"]), 1)
        self.assertIn("Data does not match any of the allowed types", result["errors"][0]["message"])

    def test_valid_enum(self):
        schema = {"enum": [123,"abc"]}
        data = "abc"
        result = self.validator.validate(data, schema, self.path, self.line)
        self.assertTrue(result["valid"])
        self.assertEqual(len(result["errors"]), 0)

    def test_enum_violation(self):
        schema = {"enum": [123,"abc"]}
        data = 2
        result = self.validator.validate(data, schema, self.path, self.line)
        self.assertFalse(result["valid"])
        self.assertEqual(len(result["errors"]), 1)
        self.assertIn("Data does not match any of the enum values", result["errors"][0]["message"])

    def test_valid_const(self):
        schema = {"const": "abc"}
        data = "abc"
        result = self.validator.validate(data, schema, self.path, self.line)
        self.assertTrue(result["valid"])
        self.assertEqual(len(result["errors"]), 0)

    def test_const_violation(self):
        schema = {"const": "abc"}
        data = "abcd"
        result = self.validator.validate(data, schema, self.path, self.line)
        self.assertFalse(result["valid"])
        self.assertEqual(len(result["errors"]), 1)
        self.assertIn("Data does not match the const value", result["errors"][0]["message"])

if __name__ == "__main__":
    unittest.main()
