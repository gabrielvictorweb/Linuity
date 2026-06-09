from linuity.application.effects.effect_factory import EffectFactory


class EffectRunner:
    def __init__(self):
        self._current_effect = None
        self._current_mode = None
        self._factory = None

    def reset(self):
        """Forces effect and factory recreation on the next run (e.g. when the device changed)."""
        self._current_effect = None
        self._current_mode = None
        self._factory = None

    def run(self, device, preset):
        mode = preset.get("mode", "led-off")

        if self._factory is None:
            self._factory = EffectFactory(device)

        if mode != self._current_mode:
            self._current_effect = self._factory.get(mode)
            self._current_mode = mode

        self._current_effect.execute(preset)
