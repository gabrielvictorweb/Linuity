from typing import Any, Dict

from linuity.application.ports.support_led_intensity import SupportsLedIntensity


class ExecWaveEffect:
    def __init__(self, device: SupportsLedIntensity):
        self._device = device
        self._pct: int = 0
        self._direction: int = 1

    def execute(self, preset: Dict[str, Any]) -> None:
        step = int(preset.get("step", 10))
        contrast = str(preset.get("contrast", "false")).lower() == "true"

        top = self._pct
        bottom = 100 - self._pct

        if contrast:
            top = int((top / 100) ** 2 * 100)
            bottom = int((bottom / 100) ** 2 * 100)

        self._device.set_led_intensity(top, bottom)

        self._pct += self._direction * step

        if self._pct >= 100:
            self._pct = 100
            self._direction = -1
        elif self._pct <= 0:
            self._pct = 0
            self._direction = 1
