import json
from pathlib import Path

CONFIG_FILE = Path(".excel_configs.json")

def save_configs(configs: dict, path: Path = CONFIG_FILE):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(configs, f, indent=2)

def load_configs(path: Path = CONFIG_FILE) -> dict:
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def apply_configs_to_state(configs: dict, session_state):
    """
    Update Streamlit widgets in session_state to reflect imported configs.
    """
    for key, cfg in configs.items():
        # key is like "filename:sheet"
        # cfg is dict with name_row, header_row, unit_row, data_row
        if cfg.get("name") is None:
            session_state[f"use_name_{key}"] = False
        else:
            session_state[f"use_name_{key}"] = True
            session_state[f"name_{key}"] = cfg.get("name", 1)

        session_state[f"header_{key}"] = cfg.get("header", 2)

        if cfg.get("unit") is None:
            session_state[f"use_unit_{key}"] = False
        else:
            session_state[f"use_unit_{key}"] = True
            session_state[f"unit_{key}"] = cfg.get("unit", 3)

        session_state[f"data_{key}"] = cfg.get("data", 4)