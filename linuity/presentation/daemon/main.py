#!/usr/bin/env python3

import logging
from pathlib import Path

import tomllib

from linuity.application.effects.effect_runner import EffectRunner
from linuity.config.config_loader import ConfigLoader
from linuity.infra.device.hyperx_device_factory import HyperXDeviceFactory
from linuity.infra.logging_config import log_separator, setup_daemon_logging
from linuity.presentation.daemon.daemon import Daemon
from linuity.presentation.daemon.device_manager import DeviceManager

setup_daemon_logging()

logger = logging.getLogger(__name__)


def load_config():
    config_file = Path("/etc/linuity/config.toml")

    if not config_file.exists():
        raise RuntimeError("Config file not found: /etc/linuity/config.toml")

    with open(config_file, "rb") as f:
        data = tomllib.load(f)

    return data["linuity"]["config_path"]


CONFIG_PATH = load_config()


def main():
    log_separator(logger)
    logger.info("Linuity Daemon  —  preset: %s", CONFIG_PATH)
    log_separator(logger)

    device_factory = HyperXDeviceFactory()
    device_manager = DeviceManager(device_factory)
    config_loader = ConfigLoader(CONFIG_PATH)
    effect_runner = EffectRunner()

    daemon = Daemon(
        config_loader=config_loader,
        device_manager=device_manager,
        effect_runner=effect_runner,
    )

    daemon.run()


if __name__ == "__main__":
    main()
