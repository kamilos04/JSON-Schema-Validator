import unittest
from backend.app.validators.arrays import ArrayValidator

class TestArrayValidator(unittest.TestCase):
    def setUp(self):
        self.validator = ArrayValidator()
        self.path = "root"
        self.line = 1

    def test_valid_array(self):
        schema = {"minItems" : 1, "maxItems" : 3}
        data = [1, "abc"]
        result = self.validator.validate(data, schema, self.path, self.line)
        self.assertTrue(result["valid"])
        self.assertEqual(len(result["errors"]), 0)

    def test_not_an_array(self):
        schema = {"maxItems" : 3}
        data = 10
        result = self.validator.validate(data, schema, self.path, self.line)
        self.assertFalse(result["valid"])
        self.assertEqual(len(result["errors"]), 1)
        self.assertIn("Data is not an array", result["errors"][0]["message"])

    def test_items_violation(self):
        schema = { "items": { "type": "number" }}
        data = ["abc"]
        result = self.validator.validate(data, schema, self.path, self.line)
        self.assertFalse(result["valid"])
        self.assertEqual(len(result["errors"]), 1)
        self.assertIn("", result["errors"][0]["message"])

    def test_minItems_violation(self):
        schema = {"minItems" : 3}
        data = [1,"abc"]
        result = self.validator.validate(data, schema, self.path, self.line)
        self.assertFalse(result["valid"])
        self.assertEqual(len(result["errors"]), 1)
        self.assertIn("Array length 2 is smaller than minItems 3", result["errors"][0]["message"])

    def test_maxItems_violation(self):
        schema = {"maxItems": 3}
        data = [1, "abc", True, 2]
        result = self.validator.validate(data, schema, self.path, self.line)
        self.assertFalse(result["valid"])
        self.assertEqual(len(result["errors"]), 1)
        self.assertIn("Array length 4 is bigger than maxItems 3", result["errors"][0]["message"])

    def test_multiple_violations(self):
        schema = {"minItems": 5, "maxItems": 3}
        data = [1, "abc", True, 2]
        result = self.validator.validate(data, schema, self.path, self.line)
        self.assertFalse(result["valid"])
        self.assertEqual(len(result["errors"]), 2)

if __name__ == "__main__":
    unittest.main()
