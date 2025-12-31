import json, os
from .constants import JSON_CONFIG

def load_json(path):
    if not os.path.exists(path):
        return {} if path == JSON_CONFIG else []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {} if path == JSON_CONFIG else []

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
