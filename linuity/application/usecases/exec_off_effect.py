from typing import Any, Dict

from linuity.application.ports.support_led_intensity import SupportsLedIntensity


class ExecOffEffect:
    def __init__(self, device: SupportsLedIntensity):
        self._device = device

    def execute(self, preset: Dict[str, Any]) -> None:
        self._device.set_led_intensity(0, 0)
