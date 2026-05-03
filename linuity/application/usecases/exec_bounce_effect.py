from typing import Any, Dict

from linuity.application.ports.support_led_intensity import SupportsLedIntensity


class ExecBounceEffect:
    def __init__(self, device: SupportsLedIntensity):
        self._device = device
        self._pos = 0
        self._direction = 1

    def execute(self, preset: Dict[str, Any]) -> None:
        step = int(preset.get("step", 1))

        # update position
        self._pos += self._direction * step

        if self._pos >= 100:
            self._pos = 100
            self._direction = -1
        elif self._pos <= 0:
            self._pos = 0
            self._direction = 1

        top = self._pos
        bottom = 100 - self._pos

        # apply curve (improves visuals)
        top = int((top / 100) ** 2 * 100)
        bottom = int((bottom / 100) ** 2 * 100)

        self._device.set_led_intensity(top, bottom)
