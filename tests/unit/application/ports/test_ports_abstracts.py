from linuity.application.ports.effect import Effect
from linuity.application.ports.support_led_intensity import SupportsLedIntensity
from linuity.application.ports.usb_communicate import UsbCommunicate
from linuity.application.ports.usb_device import UsbDevice


def test_effect_abstract_method_is_executable():
    class ConcreteEffect(Effect):
        def execute(self, preset: dict) -> None:
            Effect.execute(self, preset)

    assert ConcreteEffect().execute({}) is None


def test_supports_led_intensity_abstract_method_is_executable():
    class ConcreteIntensity(SupportsLedIntensity):
        def set_led_intensity(self, top: float, bottom: float) -> None:
            SupportsLedIntensity.set_led_intensity(self, top, bottom)

    assert ConcreteIntensity().set_led_intensity(1, 2) is None


def test_usb_communicate_abstract_method_is_executable():
    class ConcreteUsb(UsbCommunicate):
        def send(self, data: bytes) -> None:
            UsbCommunicate.send(self, data)

    assert ConcreteUsb().send(b"hi") is None


def test_usb_device_abstract_methods_are_executable():
    class ConcreteDevice(UsbDevice):
        def open(self, vendor_id: int, product_id: int) -> None:
            UsbDevice.open(self, vendor_id, product_id)

        def send(self, data: bytes) -> None:
            UsbDevice.send(self, data)

    device = ConcreteDevice()
    assert device.open(1, 2) is None
    assert device.send(b"data") is None
