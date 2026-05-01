from unittest.mock import call

from linuity.application.usecases.exec_blink_effect import ExecBlinkEffect
from linuity.application.usecases.exec_bounce_effect import ExecBounceEffect
from linuity.application.usecases.exec_flicker_effect import ExecFlickerEffect
from linuity.application.usecases.exec_gradual_effect import ExecGradualEffect
from linuity.application.usecases.exec_off_effect import ExecOffEffect
from linuity.application.usecases.exec_opacity_effect import ExecOpacityEffect
from linuity.application.usecases.exec_scanner_effect import ExecScannerEffect
from linuity.application.usecases.exec_wave_effect import ExecWaveEffect


def test_exec_blink_effect_toggles(mocker):
    device = mocker.Mock()
    effect = ExecBlinkEffect(device)

    effect.execute({"top": 80, "bottom": 20})
    effect.execute({"top": 80, "bottom": 20})

    device.set_led_intensity.assert_has_calls([call(80.0, 20.0), call(0, 0)])


def test_exec_bounce_effect_applies_curve(mocker):
    device = mocker.Mock()
    effect = ExecBounceEffect(device)

    effect.execute({"step": 60})

    device.set_led_intensity.assert_called_once_with(36, 16)


def test_exec_bounce_effect_reverses_at_bounds(mocker):
    device = mocker.Mock()
    effect = ExecBounceEffect(device)

    effect.execute({"step": 200})

    device.set_led_intensity.assert_called_once_with(100, 0)


def test_exec_bounce_effect_reverses_at_lower_bound(mocker):
    device = mocker.Mock()
    effect = ExecBounceEffect(device)
    effect._direction = -1
    effect._pos = 1

    effect.execute({"step": 5})

    device.set_led_intensity.assert_called_once_with(0, 100)
    assert effect._direction == 1


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

    effect.execute({"top": 70, "bottom": 30})

    device.set_led_intensity.assert_called_once_with(70.0, 30.0)


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


def test_exec_wave_effect_wraps(mocker):
    device = mocker.Mock()
    effect = ExecWaveEffect(device)

    for _ in range(10):
        effect.execute({})

    effect.execute({})

    last_call = device.set_led_intensity.call_args_list[-1].args
    assert last_call == (0, 100)
