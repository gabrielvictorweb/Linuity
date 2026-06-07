import pytest

from linuity.presentation.daemon.daemon import Daemon


def test_run_resets_effect_after_connecting_device(mocker):
    preset = {"mode": "bounce", "interval": "0.5", "vid": "1", "pid": "2"}

    config_loader = mocker.Mock()
    config_loader.load.return_value = preset

    device = object()
    device_manager = mocker.Mock()
    device_manager.connect.return_value = device

    effect_runner = mocker.Mock()

    mocker.patch(
        "linuity.presentation.daemon.daemon.time.sleep",
        side_effect=KeyboardInterrupt,
    )

    daemon = Daemon(config_loader, device_manager, effect_runner)

    with pytest.raises(KeyboardInterrupt):
        daemon.run()

    effect_runner.reset.assert_called_once()
    effect_runner.run.assert_called_once_with(device, preset)


def test_run_reconnects_when_device_disconnects(mocker):
    preset = {"mode": "bounce", "interval": "0.5", "vid": "1", "pid": "2"}

    config_loader = mocker.Mock()
    config_loader.load.return_value = preset

    device = object()
    device_manager = mocker.Mock()
    device_manager.connect.return_value = device
    device_manager.is_connected.return_value = False

    effect_runner = mocker.Mock()

    calls = {"n": 0}

    def fake_sleep(_):
        calls["n"] += 1
        if calls["n"] >= 2:
            raise KeyboardInterrupt

    mocker.patch("linuity.presentation.daemon.daemon.time.sleep", side_effect=fake_sleep)

    daemon = Daemon(config_loader, device_manager, effect_runner)

    with pytest.raises(KeyboardInterrupt):
        daemon.run()

    device_manager.reset.assert_called()
    assert effect_runner.reset.call_count >= 2


def test_run_does_not_reset_when_device_not_detected(mocker):
    preset = {"mode": "bounce", "interval": "0.5", "vid": "1", "pid": "2"}

    config_loader = mocker.Mock()
    config_loader.load.return_value = preset

    device_manager = mocker.Mock()
    device_manager.connect.return_value = None

    effect_runner = mocker.Mock()

    mocker.patch(
        "linuity.presentation.daemon.daemon.time.sleep",
        side_effect=KeyboardInterrupt,
    )

    daemon = Daemon(config_loader, device_manager, effect_runner)

    with pytest.raises(KeyboardInterrupt):
        daemon.run()

    effect_runner.reset.assert_not_called()
    effect_runner.run.assert_not_called()
