from linuity.presentation.cli import cli_controller


def test_save_config_uses_defaults_when_missing(monkeypatch):
    class FakePresetService:
        def __init__(self):
            self.saved = None

        def load(self):
            return None

        def save(self, *args, **kwargs):
            self.saved = (args, kwargs)

    fake_service = FakePresetService()
    monkeypatch.setattr(cli_controller, "PresetService", lambda: fake_service)

    controller = cli_controller.CLIController()
    controller.save_config(vid=1, pid=2)

    args, kwargs = fake_service.saved
    assert args == ()
    assert kwargs["mode"] == "led-off"
    assert kwargs["times"] == "10"
    assert kwargs["interval"] == "0.5"
    assert kwargs["min_val"] is None
    assert kwargs["max_val"] is None
    assert kwargs["vid"] == 1
    assert kwargs["pid"] == 2


def test_save_and_apply_uses_preset_vid_pid(monkeypatch):
    class FakePresetService:
        def __init__(self):
            self.saved = None

        def load(self):
            return {"vid": "10", "pid": "20"}

        def save(self, *args, **kwargs):
            self.saved = (args, kwargs)

    fake_service = FakePresetService()
    monkeypatch.setattr(cli_controller, "PresetService", lambda: fake_service)
    restart = monkeypatch.setattr(cli_controller.DaemonControl, "restart", lambda: None)

    controller = cli_controller.CLIController()
    controller.save_and_apply("led-off", 1, 0.1, None, None, None)

    args, kwargs = fake_service.saved
    assert args == ("led-off", 1, 0.1, None, None, None, "10", "20")
    assert restart is None


def test_show_status_delegates(monkeypatch):
    class FakePresetService:
        def __init__(self):
            self.called = False

        def show_status(self):
            self.called = True

    fake_service = FakePresetService()
    monkeypatch.setattr(cli_controller, "PresetService", lambda: fake_service)

    controller = cli_controller.CLIController()
    controller.show_status()

    assert fake_service.called is True


def test_run_test_sequence_saves_each_preset(monkeypatch):
    class FakePresetService:
        def __init__(self):
            self.saved = []

        def load(self):
            return {"vid": "1", "pid": "2"}

        def save(self, *args):
            self.saved.append(args)

    fake_service = FakePresetService()
    monkeypatch.setattr(cli_controller, "PresetService", lambda: fake_service)
    monkeypatch.setattr(cli_controller.DaemonControl, "restart", lambda: None)
    monkeypatch.setattr(cli_controller.time, "sleep", lambda _val: None)

    controller = cli_controller.CLIController()
    controller.run_test_sequence(times=1, interval=0.1)

    assert len(fake_service.saved) == 8
    assert fake_service.saved[0][0] == "blinking"
    assert fake_service.saved[-1][0] == "led-off"


def test_run_test_sequence_fixed_min_max_label(monkeypatch, capsys):
    class FakePresetService:
        def __init__(self):
            self.saved = []

        def load(self):
            return {"vid": "1", "pid": "2"}

        def save(self, *args):
            self.saved.append(args)

    fake_service = FakePresetService()
    monkeypatch.setattr(cli_controller, "PresetService", lambda: fake_service)
    monkeypatch.setattr(cli_controller.DaemonControl, "restart", lambda: None)
    monkeypatch.setattr(cli_controller.time, "sleep", lambda _val: None)

    controller = cli_controller.CLIController()
    controller.run_test_sequence(
        times=1,
        interval=0.1,
        tests=[("gradual", {"min": 10, "max": 10, "interval": 0.02})],
    )

    output = capsys.readouterr().out
    assert "fixo 10%" in output


def test_run_test_sequence_restores_preset_and_disables_daemon(monkeypatch):
    class FakePresetService:
        def __init__(self):
            self.saved = []

        def load(self):
            return {
                "mode": "wave",
                "times": "3",
                "interval": "0.4",
                "opacity": "80",
                "vid": "1",
                "pid": "2",
            }

        def save(self, *args):
            self.saved.append(args)

    fake_service = FakePresetService()
    monkeypatch.setattr(cli_controller, "PresetService", lambda: fake_service)
    monkeypatch.setattr(cli_controller.DaemonControl, "restart", lambda: None)
    disable_calls = []
    monkeypatch.setattr(cli_controller.DaemonControl, "disable", lambda: disable_calls.append(True))
    monkeypatch.setattr(cli_controller.time, "sleep", lambda _val: None)

    controller = cli_controller.CLIController()
    controller.run_test_sequence(times=1, interval=0.1, tests=[("blinking", {})])

    assert fake_service.saved[-1][0] == "wave"
    assert disable_calls == [True]
