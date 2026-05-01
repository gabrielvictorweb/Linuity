# Linuity

![Lint](https://github.com/gabrielvictorweb/linuity/actions/workflows/lint.yml/badge.svg)
![Tests](https://github.com/gabrielvictorweb/linuity/actions/workflows/tests.yml/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/gabrielvictorweb/Linuity/badge.svg?branch=main)](https://coveralls.io/github/gabrielvictorweb/Linuity?branch=main)
![Python](https://img.shields.io/badge/python-3.10--3.13-blue)
![License](https://img.shields.io/github/license/gabrielvictorweb/linuity?branch=main)

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
    - `led-off`, `blinking`, `gradual`, `wave`, `bounce`, `flicker`, `scanner`
    - `test` (runs: `blinking`, `gradual`, `wave`, `bounce`, `flicker`, `scanner`, `led-off`)

- Persistent configuration via preset file

- Background daemon for continuous effects

- Automatic device detection

- Auto-restart when USB device reconnects

- Lightweight and CLI-first design

---

## 📦 Requirements

- Linux (systemd-based)
- Python 3.8+
- `pipx`
- `python3-hid` (system package)
- `fzf`
- `udev`

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

Run without saving:

```bash
linuity --mode wave
```

Scanner effect with custom interval:

```bash
linuity --mode scanner --interval 0.08 --save
```

Gradual with min/max range:

```bash
linuity --mode gradual --min 10 --max 90 --interval 0.2 --save
```

Wave with max opacity:

```bash
linuity --mode wave --opacity 80 --interval 0.1 --save
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

Check status:

```bash
linuity --status
```

View logs:

```bash
journalctl -u linuity.service -f
```

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

- Registers a systemd service:

```
/etc/systemd/system/linuity.service
```

- Creates udev rules:

```
/etc/udev/rules.d/
```

These allow Linuity to:

- Access your USB device without permission issues
- Restart automatically when the device reconnects

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
sudo rm /etc/udev/rules.d/98-linuity-restart.rules
sudo rm /etc/udev/rules.d/99-hidraw-permissions.rules
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
