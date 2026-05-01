import os
from typing import Dict, Optional


class ConfigLoader:
    def __init__(self, path: str):
        self.path = path

    def load(self) -> Optional[Dict[str, str]]:
        if not os.path.exists(self.path):
            return None

        config = {}
        with open(self.path) as f:
            for line in f:
                if "=" not in line:
                    continue
                key, value = line.strip().split("=", 1)
                config[key] = value

        return config
