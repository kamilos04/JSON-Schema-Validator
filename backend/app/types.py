from typing import TypedDict, Dict


class Result(TypedDict):
    valid: bool
    errors: list[Dict]
