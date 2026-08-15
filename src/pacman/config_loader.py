from .models.config import ConfigFile
import json
import sys

def config_loader(config_path: str)-> ConfigFile:
    with open(config_path, "r") as f:
        json_config = json.load(f)
    config = ConfigFile.model_validate(json_config)
    return config