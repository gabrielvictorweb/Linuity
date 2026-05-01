from typing import Any, Dict

from linuity.application.ports.support_led_intensity import SupportsLedIntensity


class ExecOpacityEffect:
    def __init__(self, device: SupportsLedIntensity):
        self._device = device

    def execute(self, preset: Dict[str, Any]) -> None:
        top = float(preset.get("top", 100))
        bottom = float(preset.get("bottom", 100))

        self._device.set_led_intensity(top, bottom)
