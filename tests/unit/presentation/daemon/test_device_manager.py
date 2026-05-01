from linuity.presentation.daemon.device_manager import DeviceManager


def test_connect_returns_cached_device(mocker):
    factory = mocker.Mock()
    manager = DeviceManager(factory)
    cached = object()
    manager.device = cached

    assert manager.connect() is cached
    factory.create.assert_not_called()


def test_connect_invalid_vid_pid(mocker):
    factory = mocker.Mock()
    manager = DeviceManager(factory)

    assert manager.connect(vid="bad", pid="1") is None
    factory.create.assert_not_called()


def test_connect_handles_missing_device(mocker):
    factory = mocker.Mock()
    factory.create.return_value = None
    manager = DeviceManager(factory)

    assert manager.connect(vid=1, pid=2) is None


def test_connect_success_sets_device(mocker):
    device = object()
    factory = mocker.Mock()
    factory.create.return_value = device
    manager = DeviceManager(factory)

    assert manager.connect(vid=1, pid=2) is device
    assert manager.device is device


def test_connect_handles_exception(mocker):
    factory = mocker.Mock()
    factory.create.side_effect = RuntimeError("fail")
    manager = DeviceManager(factory)

    assert manager.connect(vid=1, pid=2) is None


def test_reset_clears_device(mocker):
    manager = DeviceManager(mocker.Mock())
    manager.device = object()

    manager.reset()

    assert manager.device is None
