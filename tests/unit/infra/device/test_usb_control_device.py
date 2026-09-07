import pytest

from linuity.infra.device import usb_control_device


class FakeUsbDevice:
    def __init__(self, written=64):
        self.written = written
        self.transfer_args = None

    def ctrl_transfer(self, *args, **kwargs):
        self.transfer_args = (args, kwargs)
        return self.written


def test_open_claims_interface_zero(monkeypatch):
    raw = FakeUsbDevice()
    claimed = []
    monkeypatch.setattr(usb_control_device.usb.core, "find", lambda **_kwargs: raw)
    monkeypatch.setattr(
        usb_control_device.usb.util,
        "claim_interface",
        lambda device, interface: claimed.append((device, interface)),
    )

    device = usb_control_device.UsbControlDevice()
    device.open(0x03F0, 0x098C)

    assert device._dev is raw
    assert claimed == [(raw, 0)]


def test_open_raises_when_controller_is_missing(monkeypatch):
    monkeypatch.setattr(usb_control_device.usb.core, "find", lambda **_kwargs: None)
    device = usb_control_device.UsbControlDevice()

    with pytest.raises(OSError, match="USB controller not found"):
        device.open(0x03F0, 0x098C)


def test_send_uses_duocast_control_transfer():
    raw = FakeUsbDevice()
    device = usb_control_device.UsbControlDevice()
    device._dev = raw
    report = bytes(64)

    device.send(report)

    args, kwargs = raw.transfer_args
    assert args == (0x21, 0x09, 0x0300, 0, report)
    assert kwargs == {"timeout": 1000}


def test_send_validates_connection_and_report_size():
    device = usb_control_device.UsbControlDevice()

    with pytest.raises(RuntimeError, match="not initialized"):
        device.send(bytes(64))

    device._dev = FakeUsbDevice()
    with pytest.raises(ValueError, match="exactly 64 bytes"):
        device.send(b"short")


def test_send_rejects_incomplete_transfer():
    device = usb_control_device.UsbControlDevice()
    device._dev = FakeUsbDevice(written=32)

    with pytest.raises(OSError, match="Incomplete USB control transfer"):
        device.send(bytes(64))


def test_close_releases_interface_and_resources(monkeypatch):
    raw = FakeUsbDevice()
    calls = []
    monkeypatch.setattr(
        usb_control_device.usb.util,
        "release_interface",
        lambda device, interface: calls.append(("release", device, interface)),
    )
    monkeypatch.setattr(
        usb_control_device.usb.util,
        "dispose_resources",
        lambda device: calls.append(("dispose", device)),
    )
    device = usb_control_device.UsbControlDevice()
    device._dev = raw
    device._claimed = True

    device.close()

    assert calls == [("release", raw, 0), ("dispose", raw)]
    assert device._dev is None
    assert device._claimed is False


def test_close_is_safe_before_open():
    usb_control_device.UsbControlDevice().close()
