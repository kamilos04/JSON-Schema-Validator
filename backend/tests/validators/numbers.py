import unittest
from backend.app.validators.numbers import NumberValidator

class TestNumberValidator(unittest.TestCase):
    def setUp(self):
        self.validator = NumberValidator()
        self.path = "root"
        self.line = 1

    def test_valid_number(self):
        schema = {"minimum": 20, "maximum": 50}
        data = 25
        result = self.validator.validate(data, schema, self.path, self.line)
        self.assertTrue(result["valid"])
        self.assertEqual(len(result["errors"]), 0)

    def test_not_a_number(self):
        schema = {"minimum": 10}
        data = True
        result = self.validator.validate(data, schema, self.path, self.line)
        self.assertFalse(result["valid"])
        self.assertEqual(len(result["errors"]), 1)
        self.assertIn("Data is not a valid finite number", result["errors"][0]["message"])

    def test_not_finite_number(self):
        schema = {"minimum": 10}
        data = float('inf')
        result = self.validator.validate(data, schema, self.path, self.line)
        self.assertFalse(result["valid"])
        self.assertEqual(len(result["errors"]), 1)
        self.assertIn("Data is not a valid finite number", result["errors"][0]["message"])


    def test_minimum_violation(self):
        schema = {"minimum": 5}
        data = 2
        result = self.validator.validate(data, schema, self.path, self.line)
        self.assertFalse(result["valid"])
        self.assertEqual(len(result["errors"]), 1)
        self.assertIn("Number 2 is smaller than minimum 5", result["errors"][0]["message"])

    def test_maximum_violation(self):
        schema = {"maximum": 5}
        data = 6
        result = self.validator.validate(data, schema, self.path, self.line)
        self.assertFalse(result["valid"])
        self.assertEqual(len(result["errors"]), 1)
        self.assertIn("Number 6 is bigger than maximum 5", result["errors"][0]["message"])

    def test_exclusive_minimum_violation(self):
        schema = {"exclusiveMinimum": 1}
        data = 1
        result = self.validator.validate(data, schema, self.path, self.line)
        self.assertFalse(result["valid"])
        self.assertEqual(len(result["errors"]), 1)
        self.assertIn("Number 1 is smaller or equal than exclusiveMinimum 1", result["errors"][0]["message"])

    def test_exclusive_maximum_violation(self):
        schema = {"exclusiveMaximum": 10}
        data = 10
        result = self.validator.validate(data, schema, self.path, self.line)
        self.assertFalse(result["valid"])
        self.assertEqual(len(result["errors"]), 1)
        self.assertIn("Number 10 is bigger or equal than exclusiveMaximum 10", result["errors"][0]["message"])

    def test_multiple_of_violation(self):
        schema = {"multipleOf": 2}
        data = 13
        result = self.validator.validate(data, schema, self.path, self.line)
        self.assertFalse(result["valid"])
        self.assertEqual(len(result["errors"]), 1)
        self.assertIn("Number 13 is not a multipleOf 2", result["errors"][0]["message"])

    def test_multiple_violations(self):
        schema = {"minimum": 10, "exclusiveMaximum": 3, "multipleOf": 2}
        data = 3
        result = self.validator.validate(data, schema, self.path, self.line)
        self.assertFalse(result["valid"])
        self.assertEqual(len(result["errors"]), 3)

if __name__ == "__main__":
    unittest.main()
