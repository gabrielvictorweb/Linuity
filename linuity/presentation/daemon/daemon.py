#!/usr/bin/env python3

import time
from typing import Optional

from linuity.application.effects.effect_runner import EffectRunner
from linuity.config.config_loader import ConfigLoader
from linuity.presentation.daemon.device_manager import DeviceManager


class Daemon:
    def __init__(
        self,
        config_loader: ConfigLoader,
        device_manager: DeviceManager,
        effect_runner: EffectRunner,
    ):
        self.config_loader = config_loader
        self.device_manager = device_manager
        self.effect_runner = effect_runner

        self._current_preset: Optional[dict] = None

    def run(self):
        device = None

        while True:
            try:
                print("[ + ] Daemon loop running...", flush=True)

                preset = self.config_loader.load()

                if not preset:
                    print("[ ! ] No preset found", flush=True)
                    time.sleep(2)
                    continue

                vid = preset.get("vid")
                pid = preset.get("pid")

                if device is not None and not self.device_manager.is_connected(vid, pid):
                    print("[ ! ] Device disconnected", flush=True)
                    self.device_manager.reset()
                    self.effect_runner.reset()
                    device = None
                    self._current_preset = None

                if device is None:
                    device = self.device_manager.connect(vid=vid, pid=pid)

                    if device is None:
                        print("[ ! ] Device not detected. Waiting...", flush=True)
                        time.sleep(2)
                        continue

                    self.effect_runner.reset()

                if preset != self._current_preset:
                    print(f"[ ✔ ] New preset loaded: {preset}", flush=True)
                    self._current_preset = preset

                interval = float(preset.get("interval", 0.3))

                self.effect_runner.run(device, preset)

                time.sleep(interval)

            except Exception as e:
                print(f"[ x ] Daemon error: {e}", flush=True)

                self.device_manager.reset()
                device = None
                self._current_preset = None

                time.sleep(2)
