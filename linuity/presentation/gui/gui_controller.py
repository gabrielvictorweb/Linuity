import logging

from linuity.infra.system.daemon_control import DaemonControl
from linuity.presentation.cli.cli_controller import CLIController

logger = logging.getLogger(__name__)

MODES = ["led-off", "static", "blinking", "wave", "gradual", "flicker", "scanner"]

# Parameters shown per mode. The view builds one widget row per parameter
# and toggles visibility based on the selected mode; apply() uses the same
# table to drop values that do not belong to the mode.
MODE_PARAMS = {
    "led-off": [],
    "static": ["max"],
    "blinking": ["max", "interval"],
    "wave": ["step", "contrast", "interval"],
    "gradual": ["min", "max", "interval"],
    "flicker": ["min", "max", "variation", "interval"],
    "scanner": ["speed", "min", "max", "interval"],
}

# Widget specs: (label, widget kind, min, max, step, default)
PARAM_SPECS = {
    "max": ("Brightness (%)", "scale", 0, 100, 1, 100),
    "min": ("Min (%)", "scale", 0, 100, 1, 0),
    "variation": ("Variation (%)", "scale", 0, 100, 1, 10),
    "interval": ("Interval (s)", "spin", 0.01, 5.0, 0.01, 0.5),
    "speed": ("Speed", "spin", 0.05, 2.0, 0.05, 0.2),
    "step": ("Step (%)", "spin", 1, 50, 1, 10),
    "contrast": ("Contrast", "switch", None, None, None, False),
}


def matches_preset(preset, mode, values):
    """Check whether mode + values are exactly what the preset already stores.

    `values` is keyed by preset parameter name ("min", "max", "interval", ...).
    Only the parameters relevant to the mode are compared; stored values are
    strings (key=value file), so numbers are compared as floats and contrast
    against the "true"/"false" convention used by PresetService.
    """
    if not preset or preset.get("mode") != mode:
        return False
    for param in MODE_PARAMS[mode]:
        stored = preset.get(param)
        current = values.get(param)
        if stored is None or current is None:
            return False
        if param == "contrast":
            if (stored == "true") != bool(current):
                return False
            continue
        try:
            if float(stored) != float(current):
                return False
        except (TypeError, ValueError):
            return False
    return True


class GUIController:
    def __init__(self):
        self.cli = CLIController()

    def load_preset(self):
        return self.cli.preset_service.load() or {}

    def apply(
        self,
        mode,
        times=10,
        interval=0.5,
        min_val=None,
        max_val=None,
        variation=None,
        speed=None,
        step=None,
        contrast=None,
    ):
        if mode not in MODES:
            raise ValueError(f"Unknown mode: {mode}")

        for name, value in (("min", min_val), ("max", max_val), ("variation", variation)):
            if value is not None and not (0 <= value <= 100):
                raise ValueError(f"{name.capitalize()} must be between 0 and 100")

        if min_val is not None and max_val is not None and min_val > max_val:
            raise ValueError("Min must be less than or equal to max")

        allowed = MODE_PARAMS[mode]
        params = {
            "min_val": min_val if "min" in allowed else None,
            "max_val": max_val if "max" in allowed else None,
            "variation": variation if "variation" in allowed else None,
            "speed": speed if "speed" in allowed else None,
            "step": step if "step" in allowed else None,
            "contrast": contrast if "contrast" in allowed else None,
        }

        self.cli.save_and_apply(
            mode,
            times,
            interval,
            None,
            params["min_val"],
            params["max_val"],
            variation=params["variation"],
            speed=params["speed"],
            step=params["step"],
            contrast=params["contrast"],
        )
        logger.info("Preset applied (%s)", mode)

    def turn_off(self):
        DaemonControl.disable()
