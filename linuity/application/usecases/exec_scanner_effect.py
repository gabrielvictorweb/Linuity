import math
from typing import Any, Dict

from linuity.application.ports.support_led_intensity import SupportsLedIntensity


class ExecScannerEffect:
    def __init__(self, device: SupportsLedIntensity):
        self._device = device
        self._t = 0.0  # continuous time

    def execute(self, preset: Dict[str, Any]) -> None:
        speed = float(preset.get("speed", 0.2))
        min_val = int(preset.get("min", 0))
        max_val = int(preset.get("max", 100))

        # smooth motion (sine) — keep _t bounded to [0, 2π) to avoid float precision loss
        self._t = (self._t + speed) % (2 * math.pi)
        value = (math.sin(self._t) + 1) / 2  # 0 -> 1

        # peak position
        top = value
        bottom = 1 - value

        # curve to create contrast (trail)
        top = top**3
        bottom = bottom**3

        # scale to range
        top = int(min_val + top * (max_val - min_val))
        bottom = int(min_val + bottom * (max_val - min_val))

        self._device.set_led_intensity(top, bottom)
