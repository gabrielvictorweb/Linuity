from typing import Any, Dict

from linuity.application.ports.support_led_intensity import SupportsLedIntensity


class ExecOpacityEffect:
    def __init__(self, device: SupportsLedIntensity):
        self._device = device

    def execute(self, preset: Dict[str, Any]) -> None:
        intensity = float(preset.get("max", 100))

        self._device.set_led_intensity(intensity, intensity)
