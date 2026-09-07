from typing import Any, Dict


class ExecDefaultEffect:
    """Release software control so the device can run its built-in lighting."""

    def __init__(self, device):
        self._device = device
        self._released = False

    def execute(self, preset: Dict[str, Any]) -> None:
        if self._released:
            return
        self._device.close()
        self._released = True
