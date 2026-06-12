import logging
import time

from linuity.config.preset_service import PresetService
from linuity.infra.logging_config import log_separator
from linuity.infra.system.daemon_control import DaemonControl

logger = logging.getLogger(__name__)


class CLIController:
    def __init__(self):
        self.preset_service = PresetService()

    def show_status(self):
        self.preset_service.show_status()

    def save_config(self, vid, pid):
        logger.info("Saving device configuration...")
        config = self.preset_service.load()

        if not config:
            logger.warning("No preset configured. Using defaults.")
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
        logger.info("Configuration saved successfully")

    def run_test_sequence(self, times, interval, tests=None):
        original_config = self.preset_service.load()
        vid_pid = original_config or {}

        if tests is None:
            tests = [
                ("blinking", {"interval": 0.01}),
                ("gradual", {"min": 0, "max": 5, "interval": 0.02}),
                ("gradual", {"min": 5, "max": 100, "interval": 0.02}),
                ("wave", {"interval": 0.02}),
                ("wave", {"contrast": True, "interval": 0.01}),
                ("flicker", {"interval": 0.02}),
                ("scanner", {"speed": 0.3, "interval": 0.02}),
                ("led-off", {}),
            ]
        total = len(tests)
        log_separator(logger)
        logger.info("Test sequence — %d steps", total)
        print()

        for i, (mode, params) in enumerate(tests, 1):
            label = mode.capitalize()
            if "min" in params and "max" in params:
                if params["min"] == params["max"]:
                    label += f" (fixed {params['min']}%)"
                else:
                    label += f" ({params['min']}% -> {params['max']}%)"
            if params.get("contrast"):
                label += " (contrast)"

            print(f"  {i}/{total}  {label} ".ljust(44, "."), end=" ", flush=True)
            self.preset_service.save(
                mode,
                times,
                interval,
                None,
                params.get("min"),
                params.get("max"),
                vid_pid.get("vid"),
                vid_pid.get("pid"),
                variation=params.get("variation"),
                speed=params.get("speed"),
                step=params.get("step"),
                contrast=params.get("contrast"),
            )
            DaemonControl.restart(quiet=True)
            time.sleep(2)
            print("ok")

        print()

        if original_config and original_config.get("mode"):
            self.preset_service.save(
                original_config.get("mode"),
                original_config.get("times"),
                original_config.get("interval"),
                original_config.get("opacity"),
                original_config.get("min"),
                original_config.get("max"),
                original_config.get("vid"),
                original_config.get("pid"),
                variation=original_config.get("variation"),
                speed=original_config.get("speed"),
                step=original_config.get("step"),
                contrast=original_config.get("contrast"),
            )
            logger.info("Original preset restored (%s)", original_config.get("mode"))
        DaemonControl.disable(quiet=True)
        logger.info("Test sequence complete")
        log_separator(logger)

    def save_and_apply(
        self, mode, times, interval, opacity, min_val, max_val,
        variation=None, speed=None, step=None, contrast=None
    ):
        config = self.preset_service.load() or {}
        vid = config.get("vid")
        pid = config.get("pid")

        self.preset_service.save(
            mode, times, interval, opacity, min_val, max_val, vid, pid,
            variation=variation, speed=speed, step=step, contrast=contrast,
        )
        DaemonControl.restart()
