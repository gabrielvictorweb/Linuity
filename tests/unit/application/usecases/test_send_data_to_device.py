from linuity.application.usecases.send_data_to_device import SendDataToDevice


def test_send_data_to_device_forwards_bytes(mocker):
    usb = mocker.Mock()
    usecase = SendDataToDevice(usb)

    payload = b"\x01\x02"
    usecase.execute(payload)

    usb.send.assert_called_once_with(payload)
