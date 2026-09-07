import logging
import threading

from linuity.application.ports.support_led_intensity import SupportsLedIntensity
from linuity.application.ports.usb_device import UsbDevice

logger = logging.getLogger(__name__)


class HyperXDuoCast(SupportsLedIntensity):
    """DuoCast two-zone RGB protocol using red as the base effect color."""

    REPORT_SIZE = 64
    REFRESH_INTERVAL = 0.05

    def __init__(self, device: UsbDevice, refresh_interval: float | None = REFRESH_INTERVAL):
        self._device = device
        self._refresh_interval = refresh_interval
        self._color_report = None
        self._refresh_error = None
        self._stop_event = threading.Event()
        self._io_lock = threading.Lock()
        self._refresh_thread = None

    def close(self) -> None:
        self._stop_event.set()
        if self._refresh_thread is not None:
            self._refresh_thread.join()
            self._refresh_thread = None
        self._device.close()

    @classmethod
    def _build_display_header(cls) -> bytes:
        report = bytearray(cls.REPORT_SIZE)
        report[0] = 0x04
        report[1] = 0xF2
        report[8] = 0x01
        return bytes(report)

    @classmethod
    def _build_color_report(cls, top: float, bottom: float) -> bytes:
        top_val = int(255 * (top / 100))
        bottom_val = int(255 * (bottom / 100))
        report = bytearray(cls.REPORT_SIZE)
        report[0:4] = bytes((0x81, top_val, 0x00, 0x00))
        report[4:8] = bytes((0x81, bottom_val, 0x00, 0x00))
        return bytes(report)

    def _send_frame(self, color_report: bytes) -> None:
        with self._io_lock:
            self._device.send(self._build_display_header())
            self._device.send(color_report)

    def _refresh_loop(self) -> None:
        while not self._stop_event.wait(self._refresh_interval):
            try:
                self._send_frame(self._color_report)
            except Exception as error:
                self._refresh_error = error
                logger.error("DuoCast display refresh failed: %s", error)
                return

    def _start_refresh(self) -> None:
        if self._refresh_interval is None or self._refresh_thread is not None:
            return
        self._refresh_thread = threading.Thread(
            target=self._refresh_loop,
            name="linuity-duocast-refresh",
            daemon=True,
        )
        self._refresh_thread.start()

    def set_led_intensity(self, top: float, bottom: float) -> None:
        if self._refresh_error is not None:
            raise OSError("DuoCast display refresh stopped") from self._refresh_error

        self._color_report = self._build_color_report(top, bottom)
        self._send_frame(self._color_report)
        self._start_refresh()

    def blink(self, top: float, bottom: float) -> None:
        self.set_led_intensity(top, bottom)
