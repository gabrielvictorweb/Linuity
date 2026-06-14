import pytest

from linuity.presentation.gui import gui_controller
from linuity.presentation.gui.gui_controller import (
    MODE_PARAMS,
    MODES,
    PARAM_SPECS,
    matches_preset,
)


class FakeCLIController:
    def __init__(self):
        self.applied = None
        self.preset_service = self

    def load(self):
        return None

    def save_and_apply(self, *args, **kwargs):
        self.applied = (args, kwargs)


@pytest.fixture
def controller(monkeypatch):
    fake_cli = FakeCLIController()
    monkeypatch.setattr(gui_controller, "CLIController", lambda: fake_cli)
    return gui_controller.GUIController(), fake_cli


def test_mode_params_covers_all_modes():
    assert set(MODE_PARAMS) == set(MODES)
    for params in MODE_PARAMS.values():
        for param in params:
            assert param in PARAM_SPECS


def test_apply_delegates_to_cli_controller(controller):
    gui, fake_cli = controller

    gui.apply("gradual", times=5, interval=0.2, min_val=10, max_val=90)

    args, kwargs = fake_cli.applied
    assert args == ("gradual", 5, 0.2, None, 10, 90)
    assert kwargs == {"variation": None, "speed": None, "step": None, "contrast": None}


def test_apply_filters_params_not_in_mode(controller):
    gui, fake_cli = controller

    gui.apply("wave", step=15, contrast=True, speed=0.5, variation=20, min_val=10, max_val=90)

    args, kwargs = fake_cli.applied
    assert kwargs["step"] == 15
    assert kwargs["contrast"] is True
    # speed/variation/min/max do not belong to wave
    assert kwargs["speed"] is None
    assert kwargs["variation"] is None
    assert args[4] is None
    assert args[5] is None


def test_apply_rejects_unknown_mode(controller):
    gui, _ = controller

    with pytest.raises(ValueError, match="Unknown mode"):
        gui.apply("bounce")


def test_apply_rejects_out_of_range_values(controller):
    gui, _ = controller

    with pytest.raises(ValueError, match="Min must be between"):
        gui.apply("gradual", min_val=-1)

    with pytest.raises(ValueError, match="Max must be between"):
        gui.apply("gradual", max_val=101)

    with pytest.raises(ValueError, match="Variation must be between"):
        gui.apply("flicker", variation=200)


def test_apply_rejects_min_greater_than_max(controller):
    gui, _ = controller

    with pytest.raises(ValueError, match="Min must be less than or equal"):
        gui.apply("gradual", min_val=80, max_val=20)


def test_turn_off_disables_daemon(controller, monkeypatch):
    gui, _ = controller
    disable_calls = []
    monkeypatch.setattr(
        gui_controller.DaemonControl, "disable", lambda **kwargs: disable_calls.append(True)
    )

    gui.turn_off()

    assert disable_calls == [True]


def test_load_preset_returns_empty_dict_when_missing(controller):
    gui, _ = controller

    assert gui.load_preset() == {}


def test_matches_preset_true_when_identical():
    preset = {"mode": "wave", "step": "15", "contrast": "true", "interval": "0.5"}

    assert matches_preset(preset, "wave", {"step": 15, "contrast": True, "interval": 0.5})


def test_matches_preset_compares_numbers_as_floats():
    preset = {"mode": "gradual", "min": "10", "max": "90", "interval": "0.5"}

    assert matches_preset(preset, "gradual", {"min": 10.0, "max": 90, "interval": 0.5})


def test_matches_preset_false_on_mode_mismatch():
    preset = {"mode": "wave", "step": "15", "contrast": "true", "interval": "0.5"}

    assert not matches_preset(preset, "static", {"max": 100})


def test_matches_preset_false_on_value_mismatch():
    preset = {"mode": "wave", "step": "15", "contrast": "true", "interval": "0.5"}

    assert not matches_preset(preset, "wave", {"step": 10, "contrast": True, "interval": 0.5})
    assert not matches_preset(preset, "wave", {"step": 15, "contrast": False, "interval": 0.5})


def test_matches_preset_false_when_param_missing():
    preset = {"mode": "wave", "step": "15", "interval": "0.5"}

    assert not matches_preset(preset, "wave", {"step": 15, "contrast": True, "interval": 0.5})


def test_matches_preset_false_on_empty_or_garbage():
    assert not matches_preset({}, "led-off", {})
    assert not matches_preset(None, "led-off", {})

    garbage = {"mode": "static", "max": "not-a-number"}
    assert not matches_preset(garbage, "static", {"max": 100})


def test_matches_preset_led_off_only_needs_mode():
    assert matches_preset({"mode": "led-off"}, "led-off", {})


def test_load_preset_returns_config(controller):
    gui, fake_cli = controller
    fake_cli.load = lambda: {"mode": "wave", "step": "15"}

    assert gui.load_preset() == {"mode": "wave", "step": "15"}
