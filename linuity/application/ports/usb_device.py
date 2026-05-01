from abc import ABC, abstractmethod


class UsbDevice(ABC):
    @abstractmethod
    def open(self, vendor_id: int, product_id: int) -> None:
        """Abre conexão com o dispositivo"""
        pass

    @abstractmethod
    def send(self, data: bytes) -> None:
        """Envia dados para o dispositivo"""
        pass
