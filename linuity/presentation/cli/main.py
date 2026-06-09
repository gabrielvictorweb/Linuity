#!/usr/bin/env python3

import argparse
import logging
import sys
from importlib.metadata import version as pkg_version

from linuity.infra.logging_config import setup_cli_logging
from linuity.infra.system.daemon_control import DaemonControl
from linuity.presentation.cli.cli_controller import CLIController
from linuity.presentation.cli.components import banner

setup_cli_logging()

logger = logging.getLogger(__name__)


def main():

    banner.show(pkg_version("linuity"))

    parser = argparse.ArgumentParser(description="HyperX LED Controller (Linuity)")

    parser.add_argument(
        "--mode",
        choices=[
            "off",
            "led-off",
            "static",
            "blinking",
            "gradual",
            "wave",
            "flicker",
            "scanner",
            "test",
        ],
        help="Lighting mode (use 'off' to disable daemon)",
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
    parser.add_argument("--config", action="store_true")
    parser.add_argument("--pid", type=int, help="Product ID")
    parser.add_argument("--vid", type=int, help="Vendor ID")

    args = parser.parse_args()
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

    if args.mode == "test":
        logger.info("Running test sequence...")
        controller.run_test_sequence(args.times, args.interval)
        return

    if args.mode == "off":
        logger.info("Disabling daemon service...")
        DaemonControl.disable()
        return

    if not args.mode:
        logger.error("You must specify a mode")
        parser.print_help()
        sys.exit(1)

    if args.save:
        controller.save_and_apply(
            args.mode, args.times, args.interval, args.opacity, args.min, args.max,
            variation=args.variation, speed=args.speed, step=args.step,
            contrast=args.contrast if args.contrast else None,
        )
    else:
        logger.warning("Use --save to apply changes")


if __name__ == "__main__":
    main()
