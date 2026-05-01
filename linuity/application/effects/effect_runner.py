from linuity.application.effects.effect_factory import EffectFactory


class EffectRunner:
    def __init__(self):
        self._current_effect = None
        self._current_mode = None

    def reset(self):
        """Força recriação do effect no próximo run (por exemplo quando o device mudou)."""
        self._current_effect = None
        self._current_mode = None

    def run(self, device, preset):
        mode = preset.get("mode", "led-off")

        # 🔥 só cria novo effect se mudou
        if mode != self._current_mode:
            factory = EffectFactory(device)
            self._current_effect = factory.get(mode)
            self._current_mode = mode

        # 🔥 executa continuamente
        self._current_effect.execute(preset)
