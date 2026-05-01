import importlib
import sys
import types

import pytest


def _load_factory_module(monkeypatch):
    fake_hid = types.SimpleNamespace(device=lambda: types.SimpleNamespace())
    monkeypatch.setitem(sys.modules, "hid", fake_hid)

    import linuity.infra.device.hid_device as hid_device

    importlib.reload(hid_device)

    import linuity.infra.device.hyperx_device_factory as factory_module

    importlib.reload(factory_module)
    return factory_module


def test_create_uses_default_vid_pid(monkeypatch):
    factory_module = _load_factory_module(monkeypatch)

    class FakeHidDevice:
        def __init__(self):
            self.open_args = None

        def open(self, vid, pid):
            self.open_args = (vid, pid)

    raw = FakeHidDevice()

    monkeypatch.setattr(factory_module, "HidDevice", lambda: raw)
    monkeypatch.setattr(factory_module, "HyperXQuadcast2", lambda dev: ("wrapped", dev))

    factory = factory_module.HyperXDeviceFactory()
    result = factory.create()

    assert result[0] == "wrapped"
    assert raw.open_args == (1008, 2479)


def test_create_uses_custom_vid_pid(monkeypatch):
    factory_module = _load_factory_module(monkeypatch)

    class FakeHidDevice:
        def __init__(self):
            self.open_args = None

        def open(self, vid, pid):
            self.open_args = (vid, pid)

    raw = FakeHidDevice()

    monkeypatch.setattr(factory_module, "HidDevice", lambda: raw)
    monkeypatch.setattr(factory_module, "HyperXQuadcast2", lambda dev: ("wrapped", dev))

    factory = factory_module.HyperXDeviceFactory()
    result = factory.create(vid="111", pid="222")

    assert result[0] == "wrapped"
    assert raw.open_args == (111, 222)


def test_create_raises_on_default_open_error(monkeypatch):
    factory_module = _load_factory_module(monkeypatch)

    class FakeHidDevice:
        def open(self, _vid, _pid):
            raise RuntimeError("open fail")

    monkeypatch.setattr(factory_module, "HidDevice", FakeHidDevice)

    factory = factory_module.HyperXDeviceFactory()

    with pytest.raises(RuntimeError):
        factory.create()


def test_create_raises_on_custom_open_error(monkeypatch):
    factory_module = _load_factory_module(monkeypatch)

    class FakeHidDevice:
        def open(self, _vid, _pid):
            raise RuntimeError("open fail")

    monkeypatch.setattr(factory_module, "HidDevice", FakeHidDevice)

    factory = factory_module.HyperXDeviceFactory()

    with pytest.raises(RuntimeError):
        factory.create(vid=1, pid=2)
