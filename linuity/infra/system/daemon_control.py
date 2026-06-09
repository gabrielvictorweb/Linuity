import logging
import subprocess

logger = logging.getLogger(__name__)


class DaemonControl:
    @staticmethod
    def restart():
        logger.info("Applying configuration to device...")

        subprocess.run(
            ["sudo", "systemctl", "restart", "linuity.service"],
            check=True,
        )

        logger.info("Configuration applied successfully")

    @staticmethod
    def disable():
        logger.info("Disabling daemon service...")

        subprocess.run(
            ["sudo", "systemctl", "disable", "--now", "linuity.service"],
            check=True,
        )

        logger.info("Daemon service disabled")
