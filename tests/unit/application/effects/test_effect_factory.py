from linuity.application.effects.effect_factory import EffectFactory
from linuity.application.usecases.exec_blink_effect import ExecBlinkEffect
from linuity.application.usecases.exec_off_effect import ExecOffEffect


def test_effect_factory_returns_expected_effects(mocker):
    device = mocker.Mock()
    factory = EffectFactory(device)

    assert isinstance(factory.get("led-off"), ExecOffEffect)
    assert isinstance(factory.get("blinking"), ExecBlinkEffect)


def test_effect_factory_defaults_to_off(mocker):
    device = mocker.Mock()
    factory = EffectFactory(device)

    assert factory.get("unknown") is factory.get("led-off")
