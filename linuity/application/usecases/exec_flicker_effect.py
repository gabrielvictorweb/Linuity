import random

from linuity.application.ports.support_led_intensity import SupportsLedIntensity


class ExecFlickerEffect:
    def __init__(self, device: SupportsLedIntensity):
        self._device = device
        self._top = 50
        self._bottom = 50

    def execute(self, preset):
        min_val = int(preset.get("min", 10))
        max_val = int(preset.get("max", 100))
        variation = int(preset.get("variation", 10))

        # pequena variação
        self._top += random.randint(-variation, variation)
        self._bottom += random.randint(-variation, variation)

        # clamp
        self._top = max(min_val, min(self._top, max_val))
        self._bottom = max(min_val, min(self._bottom, max_val))

        self._device.set_led_intensity(self._top, self._bottom)
