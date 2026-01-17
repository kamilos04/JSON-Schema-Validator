import json

from backend.app.dependencies import json_validator
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from json_source_map import calculate

app = FastAPI()


class JSONAndSchemaRequest(BaseModel):
    json_data: str = Field(..., alias="json")
    schema_data: str = Field(..., alias="schema")

@app.post("/validate")
def validate(request: JSONAndSchemaRequest):
    json_dict = json.loads(request.json_data)
    schema_dict = json.loads(request.schema_data)
    json_map = calculate(request.json_data)
    return json_validator.validate(json_dict, schema_dict, "#", "", json_map)

@app.get("/health")
def health():
    return {
        "status": "ok"
    }

