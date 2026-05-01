from linuity.config.config_loader import ConfigLoader


def test_load_returns_none_when_missing(tmp_path):
    loader = ConfigLoader(str(tmp_path / "missing.conf"))

    assert loader.load() is None


def test_load_parses_key_value_lines(tmp_path):
    path = tmp_path / "config.conf"
    path.write_text("mode=led-off\ninvalid\ninterval=0.5\n", encoding="utf-8")

    loader = ConfigLoader(str(path))

    assert loader.load() == {"mode": "led-off", "interval": "0.5"}
