from linuity.application.effects.effect_factory import EffectFactory


class EffectRunner:
    def __init__(self):
        self._current_effect = None
        self._current_mode = None

    def reset(self):
        """Forces effect recreation on the next run (for example when the device changed)."""
        self._current_effect = None
        self._current_mode = None

    def run(self, device, preset):
        mode = preset.get("mode", "led-off")

        if mode != self._current_mode:
            factory = EffectFactory(device)
            self._current_effect = factory.get(mode)
            self._current_mode = mode

        self._current_effect.execute(preset)
