from typing import Any, Dict

from linuity.application.ports.support_led_intensity import SupportsLedIntensity


class ExecGradualEffect:
    def __init__(self, device: SupportsLedIntensity):
        self._device = device
        self._pct: int | None = None
        self._direction: int = 1

    def execute(self, preset: Dict[str, Any]) -> None:
        min_opacity = int(preset.get("min", 0))
        max_opacity = int(preset.get("max", 100))

        if self._pct is None:
            self._pct = min_opacity

        self._pct = max(min_opacity, min(self._pct, max_opacity))

        self._device.set_led_intensity(self._pct, self._pct)

        self._pct += 5 * self._direction

        if self._pct >= max_opacity:
            self._pct = max_opacity
            self._direction = -1
        elif self._pct <= min_opacity:
            self._pct = min_opacity
            self._direction = 1
