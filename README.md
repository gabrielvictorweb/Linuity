[![Watch the video](https://github.com/user-attachments/assets/03329484-8408-45a3-a234-1a0f76f68074)](https://www.youtube.com/watch?v=ebCudABsVpM)
https://www.youtube.com/watch?v=ebCudABsVpM

# Linuity

![Lint](https://github.com/gabrielvictorweb/linuity/actions/workflows/lint.yml/badge.svg)
![Tests](https://github.com/gabrielvictorweb/linuity/actions/workflows/tests.yml/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/gabrielvictorweb/Linuity/badge.svg?branch=main)](https://coveralls.io/github/gabrielvictorweb/Linuity?branch=main)
![Python](https://img.shields.io/badge/python-3.10--3.13-blue)
![License](https://img.shields.io/github/license/gabrielvictorweb/linuity)

**HyperX LED controller for Linux using low-level HID communication.**

Linuity is a CLI-based tool designed to control LED effects on HyperX devices (such as the QuadCast II) using low-level HID communication on Linux.

## 🎧 Supported Devices

- HyperX QuadCast II (tested)

Other devices may work but are not officially supported.

---

## ⚡ Quick Start

```bash
git clone https://github.com/gabrielvictorweb/linuity.git
cd linuity
chmod +x install.sh
./install.sh
```

---

## 💡 Why Linuity?

- Native Linux support for HyperX devices
- Automatic recovery on USB reconnect
- Persistent LED configuration

---

## 🚀 Features

- Control LED modes:
    - `led-off`, `static`, `blinking`, `gradual`, `wave`, `flicker`, `scanner`
    - `test` (cycles through all effects and disables the daemon at the end)

- Persistent configuration via preset file

- Background daemon for continuous effects

- Automatic device detection

- Auto-restart when USB device reconnects

- Lightweight and CLI-first design

- Optional GTK interface (`linuity --mode gui`)

- Automatic update check (notifies on startup when a new GitHub release exists)

---

## 📦 Requirements

- Linux (systemd-based)
- Python 3.8+
- `pipx`
- `python3-hid` (system package)
- `fzf`
- `udev`
- `python3-gi` and `gir1.2-gtk-4.0` (optional, for the GUI)

---

## ✅ Validated Linux distributions

- Ubuntu 26.04
- Debian 13

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/gabrielvictorweb/linuity.git
cd linuity
```

---

### 2. Run the installer

```bash
chmod +x install.sh
./install.sh
```

---

### 3. During installation

<img width="1007" height="713" alt="Captura de tela de 2026-05-01 12-36-51" src="https://github.com/user-attachments/assets/4e44c373-aa04-4acb-a2c3-dd5ad03e9b00" />

You will be prompted to:

- Select your device using an interactive list (fzf)
- Choose the **Controller** device (NOT the audio device)

Example:

```
HyperX QuadCast 2 Controller
```

---

### 4. Done

<img width="1007" height="782" alt="Captura de tela de 2026-05-01 12-37-53" src="https://github.com/user-attachments/assets/ba987c00-220f-4d2a-99d8-84413db89ef0" />

If `linuity` is not found right after installation, close and open the terminal again to reload your PATH.

---

## ▶️ Usage

Apply an effect and save:

```bash
linuity --mode blinking --save
```

Run without saving (preview):

```bash
linuity --mode wave
```

Gradual breathing with min/max range:

```bash
linuity --mode gradual --min 10 --max 90 --interval 0.02 --save
```

Wave with slower step:

```bash
linuity --mode wave --step 5 --interval 0.05 --save
```

Wave with contrast curve (dramatic peaks, similar to the old `bounce` mode):

```bash
linuity --mode wave --contrast --step 1 --interval 0.05 --save
```

Scanner with custom speed and brightness range:

```bash
linuity --mode scanner --speed 0.15 --min 5 --max 100 --interval 0.05 --save
```

Flicker with custom variation:

```bash
linuity --mode flicker --variation 15 --min 40 --max 100 --interval 0.05 --save
```

Static brightness:

```bash
linuity --mode static --opacity 60 --save
```

Turn off LED:

```bash
linuity --mode led-off --save
```

Run test sequence (cycles through all effects and disables the daemon at the end):

```bash
linuity --mode test
```

Disable daemon service:

```bash
linuity --mode off
```

Open the graphical interface (GTK):

```bash
linuity --mode gui
```

The GUI lets you pick a mode, tweak only the parameters relevant to it, and apply with one click. All dependencies are installed by `install.sh` — no extra setup needed. If you installed manually, install GTK support with `sudo apt install python3-gi gir1.2-gtk-4.0` (or `pip install .[gui]`).

The installer also adds a desktop launcher: search for **Linuity** in GNOME activities to open the GUI directly. Daemon control from the GUI works without a password prompt thanks to a sudoers rule scoped exclusively to `systemctl restart/disable linuity.service` for the `linuity` group (re-login required after install).

### 🔔 Update notifications

Linuity checks GitHub for a newer release on startup. The CLI prints a warning
with the new version, and the GUI shows a banner with a link to GitHub. The
result is cached for 24h in `~/.cache/linuity/latest_version`, and any network
error is silently ignored so the check never breaks the tool.

Check status:

```bash
linuity --status
```

View logs:

```bash
journalctl -u linuity.service -f
```

---

## 🎛️ Parameters

| Parameter | Modes | Description | Default |
| --- | --- | --- | --- |
| `--mode` | all | Lighting mode | — |
| `--opacity` | `static`, `blinking` | Brightness 0–100 (shorthand for `--max`) | 100 |
| `--min` | `gradual`, `flicker`, `scanner` | Minimum brightness (0–100) | 0 |
| `--max` | `gradual`, `flicker`, `scanner` | Maximum brightness (0–100) | 100 |
| `--interval` | all animated | Seconds between each effect tick | 0.5 |
| `--step` | `wave` | Brightness step per tick | 10 |
| `--contrast` | `wave` | Apply quadratic contrast curve (dramatic peaks) | off |
| `--speed` | `scanner` | Oscillation speed (radians per tick) | 0.2 |
| `--variation` | `flicker` | Max random variation per tick | 10 |
| `--save` | all | Persist configuration and apply immediately | — |
| `--status` | — | Show current preset | — |
| `--vid` / `--pid` | — | Override USB device IDs | auto |

---

## ⚠️ About `install.sh`

The installer performs system-level configuration. This section explains why elevated privileges (`sudo`) are required and what changes are made.

### Why `sudo` is required

Linuity interacts with hardware (HID devices) and system services. To do this safely and automatically, it needs to:

- Install system dependencies
- Configure device permissions (udev)
- Register a background service (systemd)

These operations require administrator privileges.

---

## 🔐 What the installer changes

### System-level changes

- Installs required packages:
    - `pipx`
    - `python3-hid`
    - `fzf`
    - `python3-gi`
    - `gir1.2-gtk-4.0`

- Registers a systemd service:

```
/etc/systemd/system/linuity.service
```

- Creates udev rules:

```
/etc/udev/rules.d/
```

- Adds a scoped sudoers rule (passwordless daemon control from the GUI):

```
/etc/sudoers.d/linuity   (NOPASSWD only for systemctl restart/disable linuity.service)
```

These allow Linuity to:

- Access your USB device without permission issues
- Restart automatically when the device reconnects
- Restart/disable the daemon from the GUI without a password prompt

---

### User-level changes

- Installs Linuity using `pipx` (isolated environment)
- Creates configuration directory:

```
~/.config/linuity/
```

- Generates:

```
preset.conf
```

This file stores:

- Selected device (VID/PID)
- LED configuration

- Installs a GNOME desktop launcher and icon:

```
~/.local/share/applications/linuity.desktop
~/.local/share/icons/hicolor/<size>/apps/linuity.png
```

---

### Runtime behavior

- A background daemon is started via systemd
- The daemon:
    - Reads your configuration
    - Connects to the device
    - Applies LED effects continuously
    - Recovers automatically from disconnects

---

## 🧠 Why this approach

Linuity uses:

- **systemd** → reliability and auto-restart
- **udev** → proper hardware permissions
- **pipx** → isolated Python environment

This ensures:

- No manual setup after install
- No permission issues
- Consistent behavior across reboots

---

## 🧹 Uninstall (manual)

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

## 🧑‍💻 Development

See `DEVELOPMENT.md` for development setup and workflow.

---

## 👨‍💻 Author

Gabriel Victor
<https://github.com/gabrielvictorweb>

---

## 📄 License

MIT
