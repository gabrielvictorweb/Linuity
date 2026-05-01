from linuity.application.ports.usb_communicate import UsbCommunicate


class SendDataToDevice:
    def __init__(self, usb: UsbCommunicate):
        self._usb = usb

    def executar(self, data: bytes) -> None:
        self._usb.send(data)
