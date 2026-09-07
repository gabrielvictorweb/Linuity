import logging

import hid

from linuity.infra.device.hid_device import HidDevice
from linuity.infra.device.hyperx_duocast import HyperXDuoCast
from linuity.infra.device.hyperx_quadcast_two import HyperXQuadcast2
from linuity.infra.device.usb_control_device import UsbControlDevice

logger = logging.getLogger(__name__)

HYPERX_VENDOR_ID = 0x03F0
DUOCAST_CONTROLLER_PID = 0x098C
DUOCAST_AUDIO_PID = 0x0A8C
QUADCAST_2_PID = 0x09AF


class HyperXDeviceFactory:
    def is_present(self, vid=None, pid=None):
        vendor_id = int(vid) if vid is not None else HYPERX_VENDOR_ID
        product_id = int(pid) if pid is not None else QUADCAST_2_PID

        try:
            return bool(hid.enumerate(vendor_id, product_id))
        except Exception:
            return False

    def create(self, vid=None, pid=None):
        vendor_id = int(vid) if vid is not None else HYPERX_VENDOR_ID
        product_id = int(pid) if pid is not None else QUADCAST_2_PID
        if (vendor_id, product_id) == (HYPERX_VENDOR_ID, DUOCAST_AUDIO_PID):
            raise ValueError(
                "The DuoCast audio device cannot control lighting; "
                "select 'HyperX DuoCast Controller' (03f0:098c)"
            )
        is_duocast = (vendor_id, product_id) == (HYPERX_VENDOR_ID, DUOCAST_CONTROLLER_PID)
        raw = UsbControlDevice() if is_duocast else HidDevice()

        if vid is None or pid is None:
            logger.warning(
                "VID/PID not provided. Using default (%s / %s)...",
                HYPERX_VENDOR_ID,
                QUADCAST_2_PID,
            )
            try:
                raw.open(HYPERX_VENDOR_ID, QUADCAST_2_PID)
            except Exception as e:
                logger.error("Failed to open default device: %r", e)
                raise
        else:
            logger.info("Connecting to device VID: %s, PID: %s...", vid, pid)
            try:
                raw.open(vendor_id, product_id)
            except Exception as e:
                logger.error("Failed to open device VID=%s PID=%s: %r", vid, pid, e)
                raise

        logger.info("Device initialized")
        return HyperXDuoCast(raw) if is_duocast else HyperXQuadcast2(raw)
