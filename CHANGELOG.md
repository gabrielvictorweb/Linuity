# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog
and this project adheres to Semantic Versioning.

---

## v0.3.2 (2026-06-07)

### Fix

- **daemon**: restore LED effect after device reconnect
- update license badge URL in README.md

## v0.3.1 (2026-05-01)

### Fix

- **test**: streamline monkeypatching for daemon control in test_run_test_sequence

## v0.3.0 (2026-05-01)

### Feat

- **effects**: enhance test sequence to restore original configuration after execution

### Fix

- improve safety checks and user feedback in installation script
- resolve missing global config error on fresh installations
- update badge links in README.md for coverage and license

## v0.2.0 (2026-05-01)

### Feat

- add .gitignore to exclude build artifacts and cache files
- add pyproject.toml for project configuration and dependencies
- **pre-commit**: add commitizen for standardized commit message formatting
- **install**: add installation script for Linuity with systemd service and device configuration
- **service**: add systemd service file for Linuity LED Daemon and example preset configuration
- **daemon**: add DaemonControl class for managing service restart and disable
- **cli**: implement main CLI for HyperX LED Controller with argument parsing and validation
- **device**: add abstract UsbDevice class for USB device communication
- **daemon**: implement Daemon class for managing device presets and effects
- **config**: add ConfigLoader and PresetService for configuration management
- add __init__.py files for application structure and module initialization
- **cli**: add CLIController for managing presets and test sequences. And add banner display function for application branding
- **device**: implement HidDevice and HyperXQuadcast2 classes for USB device management and LED intensity control
- implement SendDataToDevice class for USB data transmission
- add abstract base classes for LED effects, intensity support, and USB communication
- **effects**: implement EffectFactory and EffectRunner classes for managing LED effects
- **effects**: add LED effect classes for blinking, bouncing, flickering, gradual, opacity, off, scanner, and wave effects
