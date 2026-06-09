import logging

import hid

from linuity.application.ports.usb_device import UsbDevice

logger = logging.getLogger(__name__)


class HidDevice(UsbDevice):
    def __init__(self):
        self._dev = None

    def open(self, vendor_id: int, product_id: int) -> None:
        self._dev = hid.device()
        self._dev.open(vendor_id, product_id)
        logger.info("HID device opened")

    def send(self, data: bytes) -> None:
        if not self._dev:
            raise RuntimeError("Device not initialized")

        self._dev.send_feature_report(data)

    def close(self) -> None:
        if self._dev:
            try:
                self._dev.close()
                logger.info("HID device connection closed")
            except Exception as e:
                logger.error("Failed to close device: %s", e)
            finally:
                self._dev = None
