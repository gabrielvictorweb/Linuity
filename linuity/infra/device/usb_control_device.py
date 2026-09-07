import logging

import usb.core
import usb.util

from linuity.application.ports.usb_device import UsbDevice

logger = logging.getLogger(__name__)


class UsbControlDevice(UsbDevice):
    """USB interface-0 transport for class-specific feature reports."""

    INTERFACE = 0
    REQUEST_TYPE = 0x21
    SET_REPORT = 0x09
    FEATURE_REPORT_ID_0 = 0x0300
    TIMEOUT_MS = 1000

    def __init__(self):
        self._dev = None
        self._claimed = False

    def open(self, vendor_id: int, product_id: int) -> None:
        device = usb.core.find(idVendor=vendor_id, idProduct=product_id)
        if device is None:
            raise OSError(f"USB controller not found (VID={vendor_id:04x}, PID={product_id:04x})")

        usb.util.claim_interface(device, self.INTERFACE)
        self._dev = device
        self._claimed = True
        logger.info("USB control interface opened")

    def send(self, data: bytes) -> None:
        if self._dev is None:
            raise RuntimeError("Device not initialized")
        if len(data) != 64:
            raise ValueError("DuoCast control reports must be exactly 64 bytes")

        written = self._dev.ctrl_transfer(
            self.REQUEST_TYPE,
            self.SET_REPORT,
            self.FEATURE_REPORT_ID_0,
            self.INTERFACE,
            data,
            timeout=self.TIMEOUT_MS,
        )
        if written != len(data):
            raise OSError(f"Incomplete USB control transfer ({written}/{len(data)} bytes)")

    def close(self) -> None:
        if self._dev is None:
            return

        try:
            if self._claimed:
                usb.util.release_interface(self._dev, self.INTERFACE)
        finally:
            usb.util.dispose_resources(self._dev)
            self._dev = None
            self._claimed = False
            logger.info("USB control interface closed")
