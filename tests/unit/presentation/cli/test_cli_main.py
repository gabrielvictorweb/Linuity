import pytest

import linuity.presentation.cli.main as cli_main


def test_main_rejects_invalid_opacity(monkeypatch, capsys):
    monkeypatch.setattr(cli_main, "pkg_version", lambda _name: "0.0.0")
    monkeypatch.setattr(cli_main.banner, "show", lambda _version: None)
    monkeypatch.setattr(cli_main, "CLIController", lambda: object())
    monkeypatch.setattr(cli_main.sys, "argv", ["prog", "--mode", "led-off", "--opacity", "200"])

    with pytest.raises(SystemExit) as exc:
        cli_main.main()

    assert exc.value.code == 1
    assert "Opacity must be between 0 and 100" in capsys.readouterr().out  # print() → stdout


def test_main_prints_help_when_no_args(monkeypatch, capsys):
    monkeypatch.setattr(cli_main, "pkg_version", lambda _name: "0.0.0")
    monkeypatch.setattr(cli_main.banner, "show", lambda _version: None)
    monkeypatch.setattr(cli_main, "CLIController", lambda: object())
    monkeypatch.setattr(cli_main.sys, "argv", ["prog"])

    with pytest.raises(SystemExit) as exc:
        cli_main.main()

    assert exc.value.code == 0
    assert "usage:" in capsys.readouterr().out.lower()


def test_main_saves_device_config(monkeypatch):
    saved = {"called": False}

    class FakeController:
        def save_config(self, _vid, _pid):
            saved["called"] = True

    monkeypatch.setattr(cli_main, "pkg_version", lambda _name: "0.0.0")
    monkeypatch.setattr(cli_main.banner, "show", lambda _version: None)
    monkeypatch.setattr(cli_main, "CLIController", lambda: FakeController())
    monkeypatch.setattr(cli_main.sys, "argv", ["prog", "--vid", "100", "--pid", "200"])

    with pytest.raises(SystemExit) as exc:
        cli_main.main()

    assert exc.value.code == 0
    assert saved["called"] is True


def test_main_disables_daemon(monkeypatch):
    called = {"disabled": False}

    class FakeController:
        pass

    def _disable():
        called["disabled"] = True

    monkeypatch.setattr(cli_main, "pkg_version", lambda _name: "0.0.0")
    monkeypatch.setattr(cli_main.banner, "show", lambda _version: None)
    monkeypatch.setattr(cli_main, "CLIController", lambda: FakeController())
    monkeypatch.setattr(cli_main.DaemonControl, "disable", _disable)
    monkeypatch.setattr(cli_main.sys, "argv", ["prog", "--mode", "off"])

    cli_main.main()

    assert called["disabled"] is True
