from linuity.infra.device.hyperx_quadcast_two import HyperXQuadcast2


def test_set_led_intensity_builds_report(mocker):
    device = mocker.Mock()
    quadcast = HyperXQuadcast2(device)

    quadcast.set_led_intensity(100, 50)

    device.send.assert_called_once()
    data = device.send.call_args.args[0]
    assert isinstance(data, (bytes, bytearray))
    assert len(data) == 64
    assert data[0] == 0x81
    assert data[1] == 255
    assert data[4] == 0x81
    assert data[5] == 127


def test_blink_builds_report(mocker):
    device = mocker.Mock()
    quadcast = HyperXQuadcast2(device)

    quadcast.blink(0, 0)

    device.send.assert_called_once()
