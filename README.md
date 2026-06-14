<!-- Replace the lines below with the GUI demo video (thumbnail + YouTube URL):
[![Watch the video](thumbnail-url)](youtube-url)
youtube-url
-->

# Linuity

![Lint](https://github.com/gabrielvictorweb/linuity/actions/workflows/lint.yml/badge.svg)
![Tests](https://github.com/gabrielvictorweb/linuity/actions/workflows/tests.yml/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/gabrielvictorweb/Linuity/badge.svg?branch=main)](https://coveralls.io/github/gabrielvictorweb/Linuity?branch=main)
![Python](https://img.shields.io/badge/python-3.10--3.13-blue)
![License](https://img.shields.io/github/license/gabrielvictorweb/linuity)

HyperX LED controller for Linux. Controls LED effects on HyperX devices via low-level HID communication, with a native GTK4 desktop interface and a full CLI for scripting and automation.

## Supported Devices

- HyperX QuadCast II (tested)

Other HyperX devices may work but are not officially supported.

---

## Interface

Linuity ships with a native GTK4 interface that lets you switch modes, adjust parameters, and apply changes with a single click. A real-time log viewer is built in, streaming the daemon output directly in the app.

To open the interface, search for **Linuity** in GNOME Activities, or run:

```bash
linuity --mode gui
```

The installer registers a desktop launcher and icon automatically — no extra setup required. Daemon control (restart / disable) works without a password prompt thanks to a sudoers rule scoped exclusively to `systemctl restart/disable linuity.service`.

---

## Quick Start

```bash
git clone https://github.com/gabrielvictorweb/linuity.git
cd linuity
chmod +x install.sh
./install.sh
```

During installation you will be prompted to select your controller device from an interactive list. Choose the entry labeled **Controller** (not the audio device):

```text
HyperX QuadCast 2 Controller
```

![Device selection during install](https://github.com/user-attachments/assets/4e44c373-aa04-4acb-a2c3-dd5ad03e9b00)

If `linuity` is not found immediately after installation, open a new terminal to reload your PATH.

---

## Features

- LED modes: `led-off`, `static`, `blinking`, `gradual`, `wave`, `flicker`, `scanner`
- Native GTK4 desktop interface with real-time log viewer
- Background daemon with automatic recovery on USB reconnect
- Persistent configuration via preset file
- Update notifications on startup (CLI and GUI)
- Full CLI for scripting and automation

---

## Requirements

- Linux (systemd-based)
- Python 3.10+
- `pipx`, `fzf`, `python3-hid`
- `python3-gi`, `gir1.2-gtk-4.0` (installed automatically by `install.sh`)

Validated on Ubuntu 26.04 and Debian 13.

---

## CLI Reference

![CLI output after installation](https://github.com/user-attachments/assets/ba987c00-220f-4d2a-99d8-84413db89ef0)

Common commands:

```bash
# Apply and save a mode
linuity --mode blinking --save

# Gradual breathing
linuity --mode gradual --min 10 --max 90 --interval 0.02 --save

# Wave with contrast curve
linuity --mode wave --contrast --step 1 --interval 0.05 --save

# Scanner
linuity --mode scanner --speed 0.15 --min 5 --max 100 --interval 0.05 --save

# Turn off LED
linuity --mode led-off --save

# Disable daemon
linuity --mode off

# Show current preset
linuity --status

# Cycle through all effects (test sequence)
linuity --mode test
```

### Parameters

| Parameter | Applicable modes | Description | Default |
| --- | --- | --- | --- |
| `--mode` | all | Lighting mode | — |
| `--opacity` | `static`, `blinking` | Brightness 0–100 (shorthand for `--max`) | 100 |
| `--min` | `gradual`, `flicker`, `scanner` | Minimum brightness (0–100) | 0 |
| `--max` | `gradual`, `flicker`, `scanner` | Maximum brightness (0–100) | 100 |
| `--interval` | all animated | Seconds between each effect tick | 0.5 |
| `--step` | `wave` | Brightness step per tick | 10 |
| `--contrast` | `wave` | Apply quadratic contrast curve | off |
| `--speed` | `scanner` | Oscillation speed (radians per tick) | 0.2 |
| `--variation` | `flicker` | Max random variation per tick | 10 |
| `--save` | all | Persist configuration and apply immediately | — |
| `--status` | — | Show current preset | — |
| `--vid` / `--pid` | — | Override USB device IDs | auto |

View daemon logs:

```bash
journalctl -u linuity.service -f
```

---

## About the Installer

`install.sh` performs system-level configuration. Below is a complete list of changes it makes.

### System changes

- Installs packages: `pipx`, `python3-hid`, `fzf`, `python3-gi`, `gir1.2-gtk-4.0`
- Registers a systemd service: `/etc/systemd/system/linuity.service`
- Creates udev rules: `/etc/udev/rules.d/99-linuity.rules`
- Adds a scoped sudoers rule: `/etc/sudoers.d/linuity` (NOPASSWD only for `systemctl restart/disable linuity.service`)

### User changes

- Installs Linuity via `pipx` (isolated environment)
- Creates `~/.config/linuity/preset.conf` (stores VID/PID and LED configuration)
- Installs a GNOME desktop launcher and icon:
  - `~/.local/share/applications/linuity.desktop`
  - `~/.local/share/icons/hicolor/<size>/apps/linuity.png`

### Why these changes are needed

Linuity uses **systemd** for reliability and auto-restart, **udev** for hardware permissions, and **pipx** for an isolated Python environment. Together they ensure no manual setup is needed after install, no permission issues, and consistent behavior across reboots.

---

## Uninstall

```bash
pipx uninstall linuity
sudo systemctl disable linuity.service
sudo rm /etc/systemd/system/linuity.service
sudo rm /etc/udev/rules.d/99-linuity.rules
sudo rm /etc/sudoers.d/linuity
rm ~/.local/share/applications/linuity.desktop
rm -f ~/.local/share/icons/hicolor/*/apps/linuity.png
```

---

## Development

See [DEVELOPMENT.md](DEVELOPMENT.md) for setup and workflow.

---

## Author

Gabriel Victor — <https://github.com/gabrielvictorweb>

## License

MIT
