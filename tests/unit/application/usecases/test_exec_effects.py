from unittest.mock import call

from linuity.application.usecases.exec_blink_effect import ExecBlinkEffect
from linuity.application.usecases.exec_flicker_effect import ExecFlickerEffect
from linuity.application.usecases.exec_gradual_effect import ExecGradualEffect
from linuity.application.usecases.exec_off_effect import ExecOffEffect
from linuity.application.usecases.exec_opacity_effect import ExecOpacityEffect
from linuity.application.usecases.exec_scanner_effect import ExecScannerEffect
from linuity.application.usecases.exec_wave_effect import ExecWaveEffect


def test_exec_blink_effect_toggles(mocker):
    device = mocker.Mock()
    effect = ExecBlinkEffect(device)

    effect.execute({"max": 80})
    effect.execute({"max": 80})

    device.set_led_intensity.assert_has_calls([call(80.0, 80.0), call(0, 0)])


def test_exec_flicker_effect_clamps_max(mocker):
    device = mocker.Mock()
    effect = ExecFlickerEffect(device)

    mocker.patch(
        "linuity.application.usecases.exec_flicker_effect.random.randint",
        side_effect=[10, 10],
    )

    effect.execute({"min": 10, "max": 20, "variation": 10})

    device.set_led_intensity.assert_called_once_with(20, 20)


def test_exec_flicker_effect_clamps_min(mocker):
    device = mocker.Mock()
    effect = ExecFlickerEffect(device)
    effect._top = 5
    effect._bottom = 5

    mocker.patch(
        "linuity.application.usecases.exec_flicker_effect.random.randint",
        side_effect=[-10, -10],
    )

    effect.execute({"min": 10, "max": 100, "variation": 10})

    device.set_led_intensity.assert_called_once_with(10, 10)


def test_exec_gradual_effect_steps_and_reverses(mocker):
    device = mocker.Mock()
    effect = ExecGradualEffect(device)

    effect.execute({"min": 0, "max": 10})
    effect.execute({"min": 0, "max": 10})
    effect.execute({"min": 0, "max": 10})

    calls = [call_item.args for call_item in device.set_led_intensity.call_args_list]
    assert calls == [(0, 0), (5, 5), (10, 10)]


def test_exec_gradual_effect_hits_min_and_flips_direction(mocker):
    device = mocker.Mock()
    effect = ExecGradualEffect(device)
    effect._pct = 10
    effect._direction = -1

    effect.execute({"min": 10, "max": 20})

    assert effect._pct == 10
    assert effect._direction == 1


def test_exec_opacity_effect_uses_preset_values(mocker):
    device = mocker.Mock()
    effect = ExecOpacityEffect(device)

    effect.execute({"max": 70})

    device.set_led_intensity.assert_called_once_with(70.0, 70.0)


def test_exec_off_effect_sets_zero(mocker):
    device = mocker.Mock()
    effect = ExecOffEffect(device)

    effect.execute({})

    device.set_led_intensity.assert_called_once_with(0, 0)


def test_exec_scanner_effect_uses_curve(mocker):
    device = mocker.Mock()
    effect = ExecScannerEffect(device)

    effect.execute({"speed": 0, "min": 0, "max": 100})

    device.set_led_intensity.assert_called_once_with(12, 12)


def test_exec_wave_effect_reaches_full_range(mocker):
    device = mocker.Mock()
    effect = ExecWaveEffect(device)

    # step=10: takes 10 calls to reach top=100 (0→10→...→100)
    for _ in range(11):
        effect.execute({})

    calls = [c.args for c in device.set_led_intensity.call_args_list]
    assert calls[0] == (0, 100)    # starts with bottom at full
    assert calls[10] == (100, 0)   # reaches top at full after 10 steps


def test_exec_wave_effect_returns_to_start(mocker):
    device = mocker.Mock()
    effect = ExecWaveEffect(device)

    # full ping-pong cycle: 0→100→0 takes 20 calls, 21st is back to (0,100)
    for _ in range(21):
        effect.execute({})

    last_call = device.set_led_intensity.call_args_list[-1].args
    assert last_call == (0, 100)


def test_exec_wave_effect_contrast_applies_curve(mocker):
    device = mocker.Mock()
    effect = ExecWaveEffect(device)
    effect._pct = 60

    effect.execute({"contrast": "true"})

    # without curve: set_led_intensity(60, 40)
    # with curve: top=(60/100)^2*100=36, bottom=(40/100)^2*100=16
    device.set_led_intensity.assert_called_once_with(36, 16)
