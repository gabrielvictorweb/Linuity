from abc import ABC, abstractmethod


class UsbDevice(ABC):
    @abstractmethod
    def open(self, vendor_id: int, product_id: int) -> None:
        """Opens a connection to the device"""
        pass

    @abstractmethod
    def send(self, data: bytes) -> None:
        """Sends data to the device"""
        pass
