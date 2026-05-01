# Linuity

![Lint](https://github.com/gabrielvictorweb/linuity/actions/workflows/lint.yml/badge.svg)
![Tests](https://github.com/gabrielvictorweb/linuity/actions/workflows/tests.yml/badge.svg)
![Coverage](https://coveralls.io/repos/github/gabrielvictorweb/linuity/badge.svg?branch=main)
![Python](https://img.shields.io/badge/python-3.10--3.13-blue)
![License](https://img.shields.io/github/license/gabrielvictorweb/linuity)
![Code Quality](https://github.com/gabrielvictorweb/linuity/actions/workflows/lint.yml/badge.svg)

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

You will be prompted to:

- Select your device using an interactive list (fzf)
- Choose the **Controller** device (NOT the audio device)

Example:

```
HyperX QuadCast 2 Controller
```

---

### 4. Done

After installation, the daemon will be running automatically.

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

Turn off LED:

```bash
linuity --mode led-off --save
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
