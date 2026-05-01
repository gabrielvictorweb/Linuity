from typing import Any, Dict

from linuity.application.ports.support_led_intensity import SupportsLedIntensity


class ExecWaveEffect:
    def __init__(self, device: SupportsLedIntensity):
        self._device = device
        self._pct: int = 0

    def execute(self, preset: Dict[str, Any]) -> None:
        self._device.set_led_intensity(self._pct, 100 - self._pct)

        self._pct = (self._pct + 10) % 100
