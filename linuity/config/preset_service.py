import logging
import os
import tempfile

CONFIG_PATH = os.path.expanduser("~/.config/linuity/preset.conf")

logger = logging.getLogger(__name__)


class PresetService:
    def __init__(self, config_path=CONFIG_PATH):
        self.config_path = config_path

    def save(
        self,
        mode,
        times,
        interval,
        opacity=None,
        min_val=None,
        max_val=None,
        vid=None,
        pid=None,
        variation=None,
        speed=None,
        step=None,
        contrast=None,
    ):
        # Normalise opacity shorthand: opacity → min=0, max=opacity
        if opacity is not None and min_val is None and max_val is None:
            min_val = 0
            max_val = opacity

        lines = [f"mode={mode}\n", f"times={times}\n", f"interval={interval}\n"]
        if min_val is not None:
            lines.append(f"min={min_val}\n")
        if max_val is not None:
            lines.append(f"max={max_val}\n")
        if vid is not None:
            lines.append(f"vid={vid}\n")
        if pid is not None:
            lines.append(f"pid={pid}\n")
        if variation is not None:
            lines.append(f"variation={variation}\n")
        if speed is not None:
            lines.append(f"speed={speed}\n")
        if step is not None:
            lines.append(f"step={step}\n")
        if contrast is not None:
            lines.append(f"contrast={str(contrast).lower()}\n")

        config_dir = os.path.dirname(self.config_path)
        os.makedirs(config_dir, exist_ok=True)
        with tempfile.NamedTemporaryFile("w", dir=config_dir, delete=False) as tmp:
            tmp.writelines(lines)
            tmp_path = tmp.name
        os.replace(tmp_path, self.config_path)

    def load(self):
        if not os.path.exists(self.config_path):
            return None
        config = {}
        with open(self.config_path) as f:
            for line in f:
                line = line.strip()
                if "=" not in line:
                    continue
                key, value = line.split("=", 1)
                config[key] = value
        return config

    def show_status(self):
        config = self.load()
        if not config:
            logger.warning("No preset configured.")
            return
        print("\nCurrent configuration:")
        print(f"Mode: {config.get('mode')}")
        print(f"Min: {config.get('min')}")
        print(f"Max: {config.get('max')}")
        print(f"Interval: {config.get('interval')}\n")
