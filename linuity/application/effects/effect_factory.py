from linuity.application.ports.usb_device import UsbDevice
from linuity.application.usecases.exec_blink_effect import ExecBlinkEffect
from linuity.application.usecases.exec_bounce_effect import ExecBounceEffect
from linuity.application.usecases.exec_flicker_effect import ExecFlickerEffect
from linuity.application.usecases.exec_gradual_effect import ExecGradualEffect
from linuity.application.usecases.exec_off_effect import ExecOffEffect
from linuity.application.usecases.exec_opacity_effect import ExecOpacityEffect
from linuity.application.usecases.exec_scanner_effect import ExecScannerEffect
from linuity.application.usecases.exec_wave_effect import ExecWaveEffect


class EffectFactory:
    def __init__(self, device: UsbDevice):
        self._effects = {
            "led-off": ExecOffEffect(device),
            "static": ExecOpacityEffect(device),
            "blinking": ExecBlinkEffect(device),
            "wave": ExecWaveEffect(device),
            "bounce": ExecBounceEffect(device),
            "gradual": ExecGradualEffect(device),
            "flicker": ExecFlickerEffect(device),
            "scanner": ExecScannerEffect(device),
        }

    def get(self, mode: str):
        return self._effects.get(mode, self._effects["led-off"])
