import unittest
from unittest.mock import Mock
from backend.app.validators.main import JSONValidator

class TestJSONValidator(unittest.TestCase):
    def setUp(self):
        self.type_validator = Mock()
        self.object_validator = Mock()
        self.array_validator = Mock()
        self.string_validator = Mock()
        self.number_validator = Mock()
        self.logic_validator = Mock()

        self.validator = JSONValidator(
            type_validator=self.type_validator,
            object_validator=self.object_validator,
            array_validator=self.array_validator,
            string_validator=self.string_validator,
            number_validator=self.number_validator,
            logic_validator=self.logic_validator
        )

        self.type_validator.validate.return_value = {"valid": True, "errors": []}
        self.object_validator.validate.return_value = {"valid": True, "errors": []}
        self.array_validator.validate.return_value = {"valid": True, "errors": []}
        self.string_validator.validate.return_value = {"valid": True, "errors": []}
        self.number_validator.validate.return_value = {"valid": True, "errors": []}
        self.logic_validator.validate.return_value = {"valid": True, "errors": []}

        self.path = "#"
        self.path_json = ""
        self.json_map = {}

    def test_type_validation_failure_stops_execution(self):
        self.type_validator.validate.return_value = {"valid": False, "errors": [{"message": "Type Error"}]}
        
        result = self.validator.validate({}, {}, self.path, self.path_json, self.json_map)
        
        self.assertFalse(result["valid"])
        self.assertEqual(result["errors"][0]["message"], "Type Error")

        self.object_validator.validate.assert_not_called()
        self.logic_validator.validate.assert_not_called()

    def test_delegates_to_object_validator(self):
        data = {"key": "value"}
        self.validator.validate(data, {}, self.path, self.path_json, self.json_map)
        
        self.object_validator.validate.assert_called_once()
        self.array_validator.validate.assert_not_called()
        self.logic_validator.validate.assert_called_once()

    def test_delegates_to_array_validator(self):
        data = [1, 2]
        self.validator.validate(data, {}, self.path, self.path_json, self.json_map)
        
        self.array_validator.validate.assert_called_once()
        self.object_validator.validate.assert_not_called()
        self.logic_validator.validate.assert_called_once()

    def test_delegates_to_string_validator(self):
        data = "test string"
        self.validator.validate(data, {}, self.path, self.path_json, self.json_map)
        
        self.string_validator.validate.assert_called_once()
        self.logic_validator.validate.assert_called_once()

    def test_delegates_to_number_validator(self):
        data = 123
        self.validator.validate(data, {}, self.path, self.path_json, self.json_map)
        
        self.number_validator.validate.assert_called_once()
        self.logic_validator.validate.assert_called_once()

    def test_boolean_does_not_trigger_number_validator(self):
        data = True
        self.validator.validate(data, {}, self.path, self.path_json, self.json_map)
        
        self.number_validator.validate.assert_not_called()
        self.logic_validator.validate.assert_called_once()

    def test_aggregates_errors(self):
        data = "bad string"
        self.string_validator.validate.return_value = {
            "valid": False, 
            "errors": [{"message": "String Error"}]
        }
        self.logic_validator.validate.return_value = {
            "valid": False, 
            "errors": [{"message": "Logic Error"}]
        }

        result = self.validator.validate(data, {}, self.path, self.path_json, self.json_map)
        
        self.assertFalse(result["valid"])
        self.assertEqual(len(result["errors"]), 2)
        messages = [e["message"] for e in result["errors"]]
        self.assertIn("String Error", messages)
        self.assertIn("Logic Error", messages)

if __name__ == "__main__":
    unittest.main()