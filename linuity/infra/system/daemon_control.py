import logging
import subprocess

logger = logging.getLogger(__name__)


class DaemonControl:
    @staticmethod
    def restart(quiet: bool = False):
        if not quiet:
            logger.info("Applying configuration to device...")

        subprocess.run(
            ["sudo", "systemctl", "restart", "linuity.service"],
            check=True,
        )

        if not quiet:
            logger.info("Configuration applied successfully")

    @staticmethod
    def disable(quiet: bool = False):
        if not quiet:
            logger.info("Disabling daemon service...")

        subprocess.run(
            ["sudo", "systemctl", "disable", "--now", "linuity.service"],
            check=True,
        )

        if not quiet:
            logger.info("Daemon service disabled")
