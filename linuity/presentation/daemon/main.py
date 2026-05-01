#!/usr/bin/env python3

from pathlib import Path

import tomllib

from linuity.application.effects.effect_runner import EffectRunner
from linuity.config.config_loader import ConfigLoader
from linuity.infra.device.hyperx_device_factory import HyperXDeviceFactory
from linuity.presentation.daemon.daemon import Daemon
from linuity.presentation.daemon.device_manager import DeviceManager


def load_config():
    config_file = Path("/etc/linuity/config.toml")

    if not config_file.exists():
        raise RuntimeError("[ x ] Config file not found")

    with open(config_file, "rb") as f:
        data = tomllib.load(f)

    return data["linuity"]["config_path"]


CONFIG_PATH = load_config()


def main():
    device_factory = HyperXDeviceFactory()
    print(CONFIG_PATH)
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
