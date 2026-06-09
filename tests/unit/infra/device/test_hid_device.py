import importlib
import sys
import types

import pytest


def _load_hid_device(monkeypatch):
    class FakeHidInner:
        def __init__(self):
            self.open_args = None
            self.sent = []
            self.closed = False

        def open(self, vid, pid):
            self.open_args = (vid, pid)

        def send_feature_report(self, data):
            self.sent.append(data)

        def close(self):
            self.closed = True

    fake_inner = FakeHidInner()
    fake_hid = types.SimpleNamespace(device=lambda: fake_inner)

    monkeypatch.setitem(sys.modules, "hid", fake_hid)

    import linuity.infra.device.hid_device as hid_device

    importlib.reload(hid_device)
    return hid_device, fake_inner


def test_hid_device_send_requires_open(monkeypatch):
    hid_device, _ = _load_hid_device(monkeypatch)
    device = hid_device.HidDevice()

    with pytest.raises(RuntimeError):
        device.send(b"hi")


def test_hid_device_open_and_send(monkeypatch):
    hid_device, fake_inner = _load_hid_device(monkeypatch)
    device = hid_device.HidDevice()

    device.open(1, 2)
    device.send(b"abc")

    assert fake_inner.open_args == (1, 2)
    assert fake_inner.sent == [b"abc"]


def test_hid_device_close(monkeypatch):
    hid_device, fake_inner = _load_hid_device(monkeypatch)
    device = hid_device.HidDevice()

    device.open(1, 2)
    device.close()

    assert fake_inner.closed is True
    assert device._dev is None


def test_hid_device_close_handles_error(monkeypatch, caplog):
    import logging

    hid_device, fake_inner = _load_hid_device(monkeypatch)
    device = hid_device.HidDevice()

    def _raise_close():
        raise RuntimeError("boom")

    fake_inner.close = _raise_close

    device.open(1, 2)
    with caplog.at_level(logging.ERROR):
        device.close()

    assert "Failed to close device" in caplog.text
    assert device._dev is None
