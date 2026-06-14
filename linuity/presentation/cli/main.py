#!/usr/bin/env python3

import argparse
import logging
import sys
from importlib.metadata import version as pkg_version
from subprocess import CalledProcessError

from linuity.application.effects.effect_factory import AVAILABLE_MODES
from linuity.infra.logging_config import setup_cli_logging
from linuity.infra.system.daemon_control import DaemonControl
from linuity.infra.update_checker import check_for_update
from linuity.presentation.cli.cli_controller import CLIController
from linuity.presentation.cli.components import banner

setup_cli_logging()

logger = logging.getLogger(__name__)


def main():

    banner.show(pkg_version("linuity"))

    update = check_for_update(pkg_version("linuity"))
    if update:
        logger.warning(
            "New version available: v%s — https://github.com/gabrielvictorweb/linuity", update
        )

    parser = argparse.ArgumentParser(description="HyperX LED Controller (Linuity)")

    parser.add_argument(
        "--mode",
        choices=[*AVAILABLE_MODES, "off", "test", "gui"],
        help="Lighting mode (use 'off' to disable daemon, 'gui' to open the interface)",
    )
    parser.add_argument("--opacity", type=int, help="Max opacity (0-100)")
    parser.add_argument("--min", type=int, help="Minimum opacity (0-100)")
    parser.add_argument("--max", type=int, help="Maximum opacity (0-100)")
    parser.add_argument("--times", type=int, default=10)
    parser.add_argument("--interval", type=float, default=0.5)
    parser.add_argument("--variation", type=int, default=None, help="Flicker variation (0-100)")
    parser.add_argument("--speed", type=float, default=None, help="Scanner speed")
    parser.add_argument("--step", type=int, default=None, help="Wave step size")
    parser.add_argument("--contrast", action="store_true", help="Apply contrast curve to wave")
    parser.add_argument("--save", action="store_true")
    parser.add_argument("--status", action="store_true")
    parser.add_argument("--pid", type=int, help="Product ID")
    parser.add_argument("--vid", type=int, help="Vendor ID")

    args = parser.parse_args()

    if args.mode == "gui":
        from linuity.presentation.gui.main import launch_gui

        sys.exit(launch_gui())

    controller = CLIController()

    # validations
    if args.opacity is not None and not (0 <= args.opacity <= 100):
        print("[ x ] Opacity must be between 0 and 100")
        sys.exit(1)

    if args.min is not None and not (0 <= args.min <= 100):
        print("[ x ] Min must be between 0 and 100")
        sys.exit(1)

    if args.max is not None and not (0 <= args.max <= 100):
        print("[ x ] Max must be between 0 and 100")
        sys.exit(1)

    if args.opacity is not None and (args.min is not None or args.max is not None):
        print("[ x ] Use opacity OR min/max, not both")
        sys.exit(1)

    # save VID/PID config
    if args.pid and args.vid:
        controller.save_config(args.vid, args.pid)
        sys.exit(0)

    # no valid args
    if not any([args.mode, args.status]):
        parser.print_help()
        sys.exit(0)

    if args.status:
        controller.show_status()
        return

    try:
        if args.mode == "test":
            controller.run_test_sequence(args.times, args.interval)
            return

        if args.mode == "off":
            logger.info("Disabling daemon service...")
            DaemonControl.disable()
            return

        if args.save:
            controller.save_and_apply(
                args.mode,
                args.times,
                args.interval,
                args.opacity,
                args.min,
                args.max,
                variation=args.variation,
                speed=args.speed,
                step=args.step,
                contrast=args.contrast or None,
            )
        else:
            logger.warning("Use --save to apply changes")
    except CalledProcessError as e:
        logger.error("Failed to control the daemon service: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
