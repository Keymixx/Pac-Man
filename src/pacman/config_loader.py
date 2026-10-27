import json

from .models.config import ConfigFile


def config_loader(config_path: str) -> ConfigFile:
    with open(config_path, "r", encoding="utf-8") as f:
        lines = [line for line in f if not line.strip().startswith("#")]

    json_config = json.loads("".join(lines))
    config = ConfigFile.model_validate(json_config)
    return config
