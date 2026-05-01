from abc import ABC, abstractmethod


class SupportsLedIntensity(ABC):
    @abstractmethod
    def set_led_intensity(self, top: float, bottom: float) -> None:
        pass
