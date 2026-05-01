import time

from linuity.config.preset_service import PresetService
from linuity.infra.system.daemon_control import DaemonControl


class CLIController:
    def __init__(self):
        self.preset_service = PresetService()

    def show_status(self):
        self.preset_service.show_status()

    def save_config(self, vid, pid):
        print("\n💾 Salvando configuração atual...\n")
        config = self.preset_service.load()

        if not config:
            print("[ ! ] No preset configured.")
            config = {
                "mode": "led-off",
                "times": "10",
                "interval": "0.5",
            }
        self.preset_service.save(
            mode=config.get("mode"),
            times=config.get("times"),
            interval=config.get("interval"),
            min_val=config.get("min"),
            max_val=config.get("max"),
            vid=vid,
            pid=pid,
        )
        print("✅ Configuração salva com sucesso!\n")

    def run_test_sequence(self, times, interval, tests=None):
        if tests is None:
            tests = [
                ("blinking", {"interval": 0.01}),
                ("gradual", {"min": 0, "max": 5, "interval": 0.02}),
                ("gradual", {"min": 5, "max": 100, "interval": 0.02}),
                ("wave", {"interval": 0.02}),
                ("bounce", {"interval": 0.01}),
                ("flicker", {"interval": 0.02}),
                ("scanner", {"variation": 10, "interval": 0.02}),
                ("led-off", {}),
            ]
        print("\n🧪 Iniciando teste completo...\n")
        for mode, params in tests:
            label = mode.capitalize()
            if "min" in params and "max" in params:
                if params["min"] == params["max"]:
                    label += f" (fixo {params['min']}%)"
                else:
                    label += f" ({params['min']}% → {params['max']}%)"
            print(f"[ + ] Modo: {label:<25} ⏳")
            self.preset_service.save(
                mode,
                times,
                interval,
                None,
                params.get("min"),
                params.get("max"),
                self.preset_service.load().get("vid"),
                self.preset_service.load().get("pid"),
            )
            DaemonControl.restart()
            time.sleep(2)
            print(f"[ ✔ ] Finalizado: {label}\n")
        print("🏁 Teste concluído!\n")

    def save_and_apply(self, mode, times, interval, opacity, min_val, max_val):
        vid = self.preset_service.load().get("vid")
        pid = self.preset_service.load().get("pid")

        self.preset_service.save(mode, times, interval, opacity, min_val, max_val, vid, pid)
        DaemonControl.restart()
