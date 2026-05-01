from abc import ABC, abstractmethod


class UsbCommunicate(ABC):
    @abstractmethod
    def send(self, data: bytes) -> None:
        """Envia dados via USB"""
        pass
