from linuity.infra.device.hid_device import HidDevice
from linuity.infra.device.hyperx_quadcast_two import HyperXQuadcast2


class HyperXDeviceFactory:
    def create(self, vid=None, pid=None):
        raw = HidDevice()

        if vid is None or pid is None:
            print("[ ! ] VID/PID not provided. Using default (1008 / 2479)...", flush=True)
            try:
                raw.open(1008, 2479)
            except Exception as e:
                print(f"[ x ] Failed to open default device: {e!r}", flush=True)
                raise
        else:
            print(f"[ + ] Connecting to device VID: {vid}, PID: {pid}...", flush=True)
            try:
                raw.open(int(vid), int(pid))
            except Exception as e:
                print(f"[ x ] Failed to open device VID={vid} PID={pid}: {e!r}", flush=True)
                raise

        print("[ ✔ ] Device initialized")
        return HyperXQuadcast2(raw)
