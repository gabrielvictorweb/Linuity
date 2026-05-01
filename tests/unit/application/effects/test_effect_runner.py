from linuity.application.effects.effect_runner import EffectRunner


def test_effect_runner_reuses_effect_for_same_mode(mocker):
    created = []

    class DummyEffect:
        def __init__(self):
            self.calls = 0

        def execute(self, preset):
            self.calls += 1

    class FactorySpy:
        def __init__(self, device):
            self.device = device
            self.effect = DummyEffect()
            self.modes = []
            created.append(self)

        def get(self, mode):
            self.modes.append(mode)
            return self.effect

    mocker.patch("linuity.application.effects.effect_runner.EffectFactory", FactorySpy)

    runner = EffectRunner()
    device = object()

    runner.run(device, {"mode": "wave"})
    runner.run(device, {"mode": "wave"})

    assert len(created) == 1
    assert created[0].modes == ["wave"]
    assert created[0].effect.calls == 2

    runner.run(device, {"mode": "led-off"})

    assert len(created) == 2
    assert created[1].modes == ["led-off"]

    runner.reset()
    runner.run(device, {"mode": "wave"})

    assert len(created) == 3
