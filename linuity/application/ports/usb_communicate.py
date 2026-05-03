from abc import ABC, abstractmethod


class UsbCommunicate(ABC):
    @abstractmethod
    def send(self, data: bytes) -> None:
        """Sends data over USB"""
        pass
