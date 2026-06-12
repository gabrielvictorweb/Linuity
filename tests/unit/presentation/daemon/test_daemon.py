import pytest

from linuity.presentation.daemon.daemon import Daemon


def _make_daemon(mocker, config_loader, device_manager, effect_runner):
    """Helper that also patches os.path.getmtime so the mtime-cache path works."""
    config_loader.path = "/fake/preset.conf"
    mocker.patch("linuity.presentation.daemon.daemon.os.path.getmtime", return_value=1.0)
    return Daemon(config_loader, device_manager, effect_runner)


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

    daemon = _make_daemon(mocker, config_loader, device_manager, effect_runner)

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

    daemon = _make_daemon(mocker, config_loader, device_manager, effect_runner)

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

    daemon = _make_daemon(mocker, config_loader, device_manager, effect_runner)

    with pytest.raises(KeyboardInterrupt):
        daemon.run()

    effect_runner.reset.assert_not_called()
    effect_runner.run.assert_not_called()


def test_load_preset_if_changed_does_not_resurrect_stale_preset(mocker):
    config_loader = mocker.Mock()
    config_loader.path = "/fake/preset.conf"
    getmtime = mocker.patch(
        "linuity.presentation.daemon.daemon.os.path.getmtime", return_value=1.0
    )

    daemon = Daemon(config_loader, mocker.Mock(), mocker.Mock())

    config_loader.load.return_value = {"mode": "wave"}
    preset = daemon._load_preset_if_changed()
    assert preset == {"mode": "wave"}
    daemon._current_preset = preset  # run() does this after loading

    # file modified with invalid/empty content
    getmtime.return_value = 2.0
    config_loader.load.return_value = None
    assert daemon._load_preset_if_changed() is None

    # subsequent iterations must keep returning None, not the old preset
    assert daemon._load_preset_if_changed() is None

    # once the file is valid again, the new preset is picked up
    config_loader.load.return_value = {"mode": "static"}
    assert daemon._load_preset_if_changed() == {"mode": "static"}
