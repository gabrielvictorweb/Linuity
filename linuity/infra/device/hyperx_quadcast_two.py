from linuity.application.ports.support_led_intensity import SupportsLedIntensity
from linuity.application.ports.usb_device import UsbDevice


class HyperXQuadcast2(SupportsLedIntensity):
    def __init__(self, device: UsbDevice):
        self._device = device

    def set_led_intensity(self, top: float, bottom: float) -> None:
        top_val = int(255 * (top / 100))
        bottom_val = int(255 * (bottom / 100))

        report = [0x81, top_val, 0x00, 0x00, 0x81, bottom_val, 0x00, 0x00] + [0x00] * 56

        data = bytes(report)
        self._device.send(data)

    def blink(self, top: float, bottom: float) -> None:
        top_val = int(255 * (top / 100))
        bottom_val = int(255 * (bottom / 100))

        report = [0x81, top_val, 0x00, 0x00, 0x81, bottom_val, 0x00, 0x00] + [0x00] * 56

        data = bytes(report)
        self._device.send(data)
