#!/usr/bin/env python3

import logging
import os
import signal
import threading
import time
from typing import Optional

from linuity.application.effects.effect_runner import EffectRunner
from linuity.config.config_loader import ConfigLoader
from linuity.infra.logging_config import log_separator
from linuity.presentation.daemon.device_manager import DeviceManager

logger = logging.getLogger(__name__)


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
        self._config_mtime: Optional[float] = None

    def _load_preset_if_changed(self) -> Optional[dict]:
        """Returns updated preset only when the config file has been modified."""
        try:
            mtime = os.path.getmtime(self.config_loader.path)
        except OSError:
            return None

        if self._current_preset is not None and mtime == self._config_mtime:
            return self._current_preset

        preset = self.config_loader.load()
        if preset is None:
            # Invalid/empty file: don't record the mtime, so the next iteration
            # retries instead of resurrecting the previous preset.
            self._current_preset = None
            return None

        self._config_mtime = mtime
        return preset

    def run(self):
        device = None
        self._stop = threading.Event()
        signal.signal(signal.SIGTERM, lambda *_: self._stop.set())
        signal.signal(signal.SIGINT, lambda *_: self._stop.set())

        while not self._stop.is_set():
            try:
                logger.debug("Daemon loop running...")

                preset = self._load_preset_if_changed()

                if not preset:
                    logger.warning("No preset found")
                    time.sleep(2)
                    continue

                vid = preset.get("vid")
                pid = preset.get("pid")

                if device is not None and not self.device_manager.is_connected(vid, pid):
                    log_separator(logger)
                    logger.warning("Device disconnected")
                    self.device_manager.reset()
                    self.effect_runner.reset()
                    device = None
                    self._current_preset = None

                if device is None:
                    device = self.device_manager.connect(vid=vid, pid=pid)

                    if device is None:
                        logger.warning("Device not detected. Waiting...")
                        time.sleep(2)
                        continue

                    self.effect_runner.reset()
                    log_separator(logger)

                if preset != self._current_preset:
                    logger.info("New preset loaded: %s", preset)
                    self._current_preset = preset

                interval = float(preset.get("interval", 0.3))

                self.effect_runner.run(device, preset)

                time.sleep(interval)

            except (KeyboardInterrupt, SystemExit):
                raise
            except Exception as e:
                logger.exception("Daemon error: %s", e)

                self.device_manager.reset()
                device = None
                self._current_preset = None

                time.sleep(2)
