import logging

from linuity.application.ports.usb_device import UsbDevice
from linuity.application.usecases.exec_blink_effect import ExecBlinkEffect
from linuity.application.usecases.exec_flicker_effect import ExecFlickerEffect
from linuity.application.usecases.exec_gradual_effect import ExecGradualEffect
from linuity.application.usecases.exec_off_effect import ExecOffEffect
from linuity.application.usecases.exec_opacity_effect import ExecOpacityEffect
from linuity.application.usecases.exec_scanner_effect import ExecScannerEffect
from linuity.application.usecases.exec_wave_effect import ExecWaveEffect

logger = logging.getLogger(__name__)

_REGISTRY = {
    "led-off": ExecOffEffect,
    "static": ExecOpacityEffect,
    "blinking": ExecBlinkEffect,
    "wave": ExecWaveEffect,
    "gradual": ExecGradualEffect,
    "flicker": ExecFlickerEffect,
    "scanner": ExecScannerEffect,
}

AVAILABLE_MODES = list(_REGISTRY.keys())


class EffectFactory:
    def __init__(self, device: UsbDevice):
        self._device = device
        self._cache: dict = {}

    def get(self, mode: str):
        if mode not in _REGISTRY:
            logger.warning("Unknown mode %r, falling back to 'led-off'", mode)
            mode = "led-off"
        if mode not in self._cache:
            self._cache[mode] = _REGISTRY[mode](self._device)
        return self._cache[mode]
