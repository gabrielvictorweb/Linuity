import hid

from linuity.application.ports.usb_device import UsbDevice


class HidDevice(UsbDevice):
    def __init__(self):
        self._dev = None

    def open(self, vendor_id: int, product_id: int):
        self._dev = hid.device()
        self._dev.open(vendor_id, product_id)
        print("[ ✔ ] HID device opened")

    def send(self, data: bytes) -> None:
        if not self._dev:
            raise RuntimeError("[ x ] Device not initialized")

        self._dev.send_feature_report(data)

    def close(self):
        if self._dev:
            try:
                self._dev.close()
                print("[ ! ] HID device connection closed")
            except Exception as e:
                print(f"[ x ] Failed to close device: {e}")
            finally:
                self._dev = None
