import logging

logger = logging.getLogger(__name__)


class DeviceManager:
    def __init__(self, device_factory):
        self.device_factory = device_factory
        self.device = None

    def connect(self, vid=None, pid=None):
        if self.device:
            return self.device

        logger.info("Connecting to device...")

        try:
            vid_int = int(vid) if vid is not None else None
            pid_int = int(pid) if pid is not None else None
        except Exception:
            logger.error("Invalid VID/PID format")
            return None

        try:
            device = self.device_factory.create(vid=vid_int, pid=pid_int)

            if not device:
                logger.warning("Device not found")
                return None

            self.device = device
            logger.info("Device connected")
            return self.device

        except Exception as e:
            logger.error("Failed to connect to device: %s", e)
            return None

    def is_connected(self, vid=None, pid=None):
        return self.device_factory.is_present(vid=vid, pid=pid)

    def reset(self):
        logger.warning("Resetting device connection...")

        if self.device is not None:
            try:
                self.device.close()
            except Exception as e:
                logger.error("Failed to close device: %s", e)

        self.device = None
