class DeviceManager:
    def __init__(self, device_factory):
        self.device_factory = device_factory
        self.device = None

    def connect(self, vid=None, pid=None):
        if self.device:
            return self.device

        print("[ + ] Connecting to device...", flush=True)

        try:
            vid_int = int(vid) if vid is not None else None
            pid_int = int(pid) if pid is not None else None
        except Exception:
            print("[ x ] Invalid VID/PID format", flush=True)
            return None

        try:
            device = self.device_factory.create(vid=vid_int, pid=pid_int)

            if not device:
                print("[ ! ] Device not found", flush=True)
                return None

            self.device = device
            print("[ ✔ ] Device connected", flush=True)
            return self.device

        except Exception as e:
            print(f"[ x ] Failed to connect to device: {e}", flush=True)
            return None

    def is_connected(self, vid=None, pid=None):
        return self.device_factory.is_present(vid=vid, pid=pid)

    def reset(self):
        print("[ ! ] Resetting device connection...", flush=True)

        if self.device is not None:
            try:
                self.device.close()
            except Exception as e:
                print(f"[ x ] Failed to close device: {e}", flush=True)

        self.device = None
