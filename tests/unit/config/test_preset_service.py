from linuity.config.preset_service import PresetService


def test_save_and_load_with_opacity(tmp_path):
    path = tmp_path / "preset.conf"
    service = PresetService(str(path))

    service.save("static", 10, 0.5, opacity=80)

    data = service.load()
    assert data["mode"] == "static"
    assert data["times"] == "10"
    assert data["interval"] == "0.5"
    assert data["min"] == "0"
    assert data["max"] == "80"


def test_save_and_load_with_min_max_and_vid_pid(tmp_path):
    path = tmp_path / "preset.conf"
    service = PresetService(str(path))

    service.save("blinking", 5, 0.1, min_val=10, max_val=90, vid=123, pid=456)

    data = service.load()
    assert data["mode"] == "blinking"
    assert data["min"] == "10"
    assert data["max"] == "90"
    assert data["vid"] == "123"
    assert data["pid"] == "456"


def test_show_status_when_missing_config(tmp_path, caplog):
    service = PresetService(str(tmp_path / "missing.conf"))

    service.show_status()

    assert "No preset configured." in caplog.text


def test_save_and_load_new_effect_params(tmp_path):
    path = tmp_path / "preset.conf"
    service = PresetService(str(path))

    service.save(
        "wave", 1, 0.02,
        variation=20, speed=0.3, step=5, contrast=True,
    )

    data = service.load()
    assert data["variation"] == "20"
    assert data["speed"] == "0.3"
    assert data["step"] == "5"
    assert data["contrast"] == "true"


def test_load_skips_lines_without_equals(tmp_path):
    path = tmp_path / "preset.conf"
    path.write_text("mode=wave\nmalformed_line\nstep=5\n", encoding="utf-8")
    service = PresetService(str(path))

    data = service.load()
    assert data["mode"] == "wave"
    assert data["step"] == "5"
    assert "malformed_line" not in data


def test_show_status_prints_config(tmp_path, capsys):
    path = tmp_path / "preset.conf"
    path.write_text(
        "mode=wave\nmin=10\nmax=90\ninterval=0.5\n",
        encoding="utf-8",
    )
    service = PresetService(str(path))

    service.show_status()

    output = capsys.readouterr().out
    assert "Current configuration:" in output
    assert "Mode: wave" in output
    assert "Min: 10" in output
    assert "Max: 90" in output
    assert "Interval: 0.5" in output
