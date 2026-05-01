import os

CONFIG_PATH = os.path.expanduser("~/.config/linuity/preset.conf")


class PresetService:
    def __init__(self, config_path=CONFIG_PATH):
        self.config_path = config_path

    def save(
        self, mode, times, interval, opacity=None, min_val=None, max_val=None, vid=None, pid=None
    ):
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, "w") as f:
            f.write(f"mode={mode}\n")
            f.write(f"times={times}\n")
            f.write(f"interval={interval}\n")
            if min_val is not None:
                f.write(f"min={min_val}\n")
            if max_val is not None:
                f.write(f"max={max_val}\n")
            elif opacity is not None:
                f.write("min=0\n")
                f.write(f"max={opacity}\n")
            if vid is not None:
                f.write(f"vid={vid}\n")
            if pid is not None:
                f.write(f"pid={pid}\n")

    def load(self):
        if not os.path.exists(self.config_path):
            return None
        config = {}
        with open(self.config_path) as f:
            for line in f:
                key, value = line.strip().split("=")
                config[key] = value
        return config

    def show_status(self):
        config = self.load()
        if not config:
            print("⚠️ Nenhum preset configurado.")
            return
        print("\n📌 Configuração atual:")
        print(f"Modo: {config.get('mode')}")
        print(f"Min: {config.get('min')}")
        print(f"Max: {config.get('max')}")
        print(f"Interval: {config.get('interval')}\n")
