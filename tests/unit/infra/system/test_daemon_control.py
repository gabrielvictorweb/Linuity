from linuity.infra.system.daemon_control import DaemonControl


def test_daemon_control_restart_calls_systemctl(mocker):
    run = mocker.patch("linuity.infra.system.daemon_control.subprocess.run")

    DaemonControl.restart()

    run.assert_called_once_with(
        ["sudo", "systemctl", "restart", "linuity.service"],
        check=True,
    )


def test_daemon_control_disable_calls_systemctl(mocker):
    run = mocker.patch("linuity.infra.system.daemon_control.subprocess.run")

    DaemonControl.disable()

    run.assert_called_once_with(
        ["sudo", "systemctl", "disable", "--now", "linuity.service"],
        check=True,
    )
