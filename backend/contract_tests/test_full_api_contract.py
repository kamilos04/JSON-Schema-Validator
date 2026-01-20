import pytest
import requests
import json

API_URL = "http://localhost:8000/validate"

def validate_request(schema, data):
    payload = {
        "schema": json.dumps(schema),
        "json": json.dumps(data)
    }
    response = requests.post(API_URL, json=payload)
    return response

def test_types_enum_const():
    schema = {
        "type": "object",
        "properties": {
            "status": {"enum": ["active", "inactive"]},
            "version": {"const": 1},
            "count": {"type": "integer"}
        }
    }

    valid_data = {"status": "active", "version": 1, "count": 10}
    resp = validate_request(schema, valid_data)
    assert resp.status_code == 200
    assert resp.json()["valid"] is True

    invalid_data = {"status": "pending", "version": 2, "count": "ten"}
    resp = validate_request(schema, invalid_data)
    result = resp.json()
    assert result["valid"] is False
    assert len(result["errors"]) >= 3

def test_objects_validation():
    schema = {
        "type": "object",
        "required": ["id", "meta"],
        "minProperties": 2,
        "maxProperties": 3,
        "properties": {
            "id": {"type": "integer"},
            "meta": {"type": "string"}
        },
        "additionalProperties": False
    }

    resp = validate_request(schema, {"id": 1, "meta": "info"})
    assert resp.json()["valid"] is True

    resp = validate_request(schema, {"id": 1, "extra": "field"}) 
    result = resp.json()
    assert result["valid"] is False
    
    messages = [e["message"] for e in result["errors"]]
    assert any("Missing required property: meta" in m for m in messages)
    assert any("Additional property 'extra' is not allowed" in m for m in messages)

def test_arrays_validation():
    schema = {
        "type": "array",
        "minItems": 2,
        "maxItems": 4,
        "items": {
            "type": "integer"
        }
    }

    resp = validate_request(schema, [1, 2, 3])
    assert resp.json()["valid"] is True

    resp = validate_request(schema, [1, "string"])
    result = resp.json()
    assert result["valid"] is False
    assert any("Data does not match any of the allowed types" in e["message"] for e in result["errors"])

    resp = validate_request(schema, [1])
    assert "smaller than minItems" in resp.json()["errors"][0]["message"]

def test_strings_validation():
    schema = {
        "type": "string",
        "minLength": 3,
        "maxLength": 5,
        "pattern": "^[a-z]+$"
    }

    assert validate_request(schema, "abc").json()["valid"] is True

    resp = validate_request(schema, "AB")
    result = resp.json()
    assert result["valid"] is False
    messages = [e["message"] for e in result["errors"]]
    assert any("minLength" in m for m in messages)
    assert any("does not match pattern" in m for m in messages)

def test_numbers_validation():
    schema = {
        "type": "integer",
        "minimum": 10,
        "exclusiveMaximum": 20,
        "multipleOf": 2
    }

    assert validate_request(schema, 10).json()["valid"] is True
    assert validate_request(schema, 18).json()["valid"] is True

    resp = validate_request(schema, 20)
    assert "bigger or equal than exclusiveMaximum" in resp.json()["errors"][0]["message"]

    resp = validate_request(schema, 15)
    assert "not a multipleOf" in resp.json()["errors"][0]["message"]

def test_logic_operators():
    schema = {
        "allOf": [
            {"type": "integer"},
            {"minimum": 5}
        ],
        "oneOf": [
            {"multipleOf": 3},
            {"multipleOf": 5}
        ],
        "not": {"const": 15}
    }

    assert validate_request(schema, 6).json()["valid"] is True

    assert validate_request(schema, 10).json()["valid"] is True

    resp = validate_request(schema, 15)
    result = resp.json()
    assert result["valid"] is False
    messages = [e["message"] for e in result["errors"]]
    assert "Data matches more than one oneOf schema" in messages
    assert "Data matches not schema" in messages

def test_conditional_logic():
    schema = {
        "if": {"properties": {"country": {"const": "US"}}},
        "then": {"properties": {"zip": {"pattern": "^\\d{5}$"}}},
        "else": {"properties": {"zip": {"type": "string"}}}
    }

    assert validate_request(schema, {"country": "US", "zip": "12345"}).json()["valid"] is True

    resp = validate_request(schema, {"country": "US", "zip": "abc"})
    assert resp.json()["valid"] is False
    assert "does not match pattern" in resp.json()["errors"][0]["message"]

    assert validate_request(schema, {"country": "PL", "zip": "00-001"}).json()["valid"] is True

def test_complex_mixed_scenario():
    schema = {
        "type": "object",
        "required": ["users"],
        "properties": {
            "users": {
                "type": "array",
                "minItems": 1,
                "items": {
                    "type": "object",
                    "required": ["name", "role"],
                    "properties": {
                        "name": {
                            "type": "string", 
                            "minLength": 2
                        },
                        "role": {
                            "enum": ["admin", "user", "guest"]
                        },
                        "age": {
                            "type": "integer",
                            "minimum": 0
                        },
                        "contact": {
                            "oneOf": [
                                {"properties": {"email": {"type": "string", "pattern": "@"}}, "required": ["email"]},
                                {"properties": {"phone": {"type": "string", "minLength": 9}}, "required": ["phone"]}
                            ]
                        }
                    }
                }
            }
        }
    }

    valid_data = {
        "users": [
            {
                "name": "Alice",
                "role": "admin",
                "contact": {"email": "alice@example.com"}
            },
            {
                "name": "Bob",
                "role": "user",
                "age": 30,
                "contact": {"phone": "123456789"}
            }
        ]
    }
    assert validate_request(schema, valid_data).json()["valid"] is True

    invalid_data = {
        "users": [
            {
                "name": "A",
                "role": "superadmin",
                "contact": {}
            }
        ]
    }
    resp = validate_request(schema, invalid_data)
    result = resp.json()
    assert result["valid"] is False

    errors_str = json.dumps(result["errors"])
    assert "minLength" in errors_str
    assert "enum" in errors_str
    assert "oneOf" in errors_str

if __name__ == "__main__":
    pytest.main([__file__])