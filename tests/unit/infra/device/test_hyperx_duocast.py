from unittest.mock import call

import pytest

from linuity.infra.device.hyperx_duocast import HyperXDuoCast


def test_set_led_intensity_sends_header_then_color_report(mocker):
    device = mocker.Mock()
    duocast = HyperXDuoCast(device, refresh_interval=None)

    duocast.set_led_intensity(100, 50)

    header, color = [item.args[0] for item in device.send.call_args_list]
    assert len(header) == 64
    assert header[:9] == bytes((0x04, 0xF2, 0, 0, 0, 0, 0, 0, 1))
    assert len(color) == 64
    assert color[:8] == bytes((0x81, 255, 0, 0, 0x81, 127, 0, 0))
    assert device.send.call_args_list == [call(header), call(color)]


def test_blink_uses_display_sequence(mocker):
    device = mocker.Mock()
    duocast = HyperXDuoCast(device, refresh_interval=None)

    duocast.blink(0, 0)

    assert device.send.call_count == 2
    assert device.send.call_args_list[-1].args[0][:8] == bytes((0x81, 0, 0, 0, 0x81, 0, 0, 0))


def test_refresh_thread_starts_once_and_is_joined_on_close(mocker):
    device = mocker.Mock()
    threads = []

    class FakeThread:
        def __init__(self, **kwargs):
            self.kwargs = kwargs
            self.started = False
            self.joined = False
            threads.append(self)

        def start(self):
            self.started = True

        def join(self):
            self.joined = True

    mocker.patch("linuity.infra.device.hyperx_duocast.threading.Thread", FakeThread)
    duocast = HyperXDuoCast(device)

    duocast.set_led_intensity(10, 20)
    duocast.set_led_intensity(20, 30)
    duocast.close()

    assert len(threads) == 1
    assert threads[0].started is True
    assert threads[0].joined is True
    assert threads[0].kwargs["name"] == "linuity-duocast-refresh"
    device.close.assert_called_once()


def test_refresh_loop_repeats_latest_frame(mocker):
    device = mocker.Mock()
    duocast = HyperXDuoCast(device, refresh_interval=0.05)
    duocast._color_report = duocast._build_color_report(25, 75)
    waits = iter((False, True))
    duocast._stop_event.wait = mocker.Mock(side_effect=lambda _interval: next(waits))

    duocast._refresh_loop()

    assert device.send.call_count == 2
    assert device.send.call_args_list[-1].args[0][1] == int(255 * 0.25)


def test_refresh_error_is_raised_by_next_effect_tick(mocker):
    device = mocker.Mock()
    error = RuntimeError("transfer failed")
    device.send.side_effect = error
    duocast = HyperXDuoCast(device, refresh_interval=0.05)
    duocast._color_report = duocast._build_color_report(50, 50)
    duocast._stop_event.wait = mocker.Mock(return_value=False)

    duocast._refresh_loop()

    with pytest.raises(OSError, match="display refresh stopped") as exc:
        duocast.set_led_intensity(50, 50)

    assert exc.value.__cause__ is error
