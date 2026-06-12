from typing import Any, Dict

from linuity.application.ports.support_led_intensity import SupportsLedIntensity


class ExecBlinkEffect:
    def __init__(self, device: SupportsLedIntensity):
        self._device = device
        self._state: bool = False

    def execute(self, preset: Dict[str, Any]) -> None:
        intensity = float(preset.get("max", 100))

        self._state = not self._state

        if self._state:
            self._device.set_led_intensity(intensity, intensity)
        else:
            self._device.set_led_intensity(0, 0)
