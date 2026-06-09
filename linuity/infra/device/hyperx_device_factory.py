import logging

import hid

from linuity.infra.device.hid_device import HidDevice
from linuity.infra.device.hyperx_quadcast_two import HyperXQuadcast2

logger = logging.getLogger(__name__)


class HyperXDeviceFactory:
    def is_present(self, vid=None, pid=None):
        vendor_id = int(vid) if vid is not None else 1008
        product_id = int(pid) if pid is not None else 2479

        try:
            return bool(hid.enumerate(vendor_id, product_id))
        except Exception:
            return False

    def create(self, vid=None, pid=None):
        raw = HidDevice()

        if vid is None or pid is None:
            logger.warning("VID/PID not provided. Using default (1008 / 2479)...")
            try:
                raw.open(1008, 2479)
            except Exception as e:
                logger.error("Failed to open default device: %r", e)
                raise
        else:
            logger.info("Connecting to device VID: %s, PID: %s...", vid, pid)
            try:
                raw.open(int(vid), int(pid))
            except Exception as e:
                logger.error("Failed to open device VID=%s PID=%s: %r", vid, pid, e)
                raise

        logger.info("Device initialized")
        return HyperXQuadcast2(raw)
