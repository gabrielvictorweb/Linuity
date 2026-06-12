from linuity.application.ports.usb_device import UsbDevice
from linuity.application.usecases.exec_blink_effect import ExecBlinkEffect
from linuity.application.usecases.exec_flicker_effect import ExecFlickerEffect
from linuity.application.usecases.exec_gradual_effect import ExecGradualEffect
from linuity.application.usecases.exec_off_effect import ExecOffEffect
from linuity.application.usecases.exec_opacity_effect import ExecOpacityEffect
from linuity.application.usecases.exec_scanner_effect import ExecScannerEffect
from linuity.application.usecases.exec_wave_effect import ExecWaveEffect

_REGISTRY = {
    "led-off": ExecOffEffect,
    "static": ExecOpacityEffect,
    "blinking": ExecBlinkEffect,
    "wave": ExecWaveEffect,
    "gradual": ExecGradualEffect,
    "flicker": ExecFlickerEffect,
    "scanner": ExecScannerEffect,
}


class EffectFactory:
    def __init__(self, device: UsbDevice):
        self._device = device
        self._cache: dict = {}

    def get(self, mode: str):
        actual = mode if mode in _REGISTRY else "led-off"
        if actual not in self._cache:
            self._cache[actual] = _REGISTRY[actual](self._device)
        return self._cache[actual]
