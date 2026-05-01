#!/bin/bash
set -e

# Colors
GREEN="\033[1;32m"
RED="\033[1;31m"
YELLOW="\033[1;33m"
CYAN="\033[1;36m"
RESET="\033[0m"

echo ""
echo "======================================="
echo " Linuity Installer (Final)"
echo "======================================="
echo ""

echo -e "${YELLOW}[ ! ] This installation requires sudo.${RESET}"
echo ""

cd "$(dirname "$0")"

# =======================================
# DEPENDENCIES
# =======================================

echo -e "${CYAN}[ + ] Installing dependencies...${RESET}"
sudo apt update
sudo apt install -y pipx python3-hid fzf

pipx ensurepath

# =======================================
# INSTALL LINUITY
# =======================================

echo -e "${CYAN}[ + ] Installing Linuity...${RESET}"

pipx uninstall linuity 2>/dev/null || true
pipx install . --force
pipx runpip linuity install hidapi

DAEMON_PATH="$HOME/.local/bin/linuity-daemon"

if [ ! -f "$DAEMON_PATH" ]; then
    echo -e "${RED}[ x ] Daemon not found${RESET}"
    exit 1
fi

# =======================================
# USER CONFIG
# =======================================

mkdir -p "$HOME/.config/linuity"

CONFIG_FILE="$HOME/.config/linuity/preset.conf"

if [ ! -f "$CONFIG_FILE" ]; then
    cp linuity/resources/preset.conf.example "$CONFIG_FILE"
fi

# =======================================
# GLOBAL CONFIG (/etc)
# =======================================

echo -e "${CYAN}[ + ] Creating global config...${RESET}"

sudo mkdir -p /etc/linuity

sudo tee /etc/linuity/config.toml > /dev/null <<EOF
[linuity]
config_path = "~/.config/linuity/preset.conf"
EOF

sudo chmod 644 /etc/linuity/config.toml

echo -e "${GREEN}[ ✔ ] Global config ready${RESET}"
echo ""

# =======================================
# DEVICE SELECTION (FZF)
# =======================================

echo -e "${CYAN}[ + ] Select your controller device:${RESET}"
echo ""

DEVICE=$(lsusb | fzf --prompt="Controller > " --height=15 --border)

if [ -z "$DEVICE" ]; then
    echo -e "${RED}[ x ] No device selected${RESET}"
    exit 1
fi

echo -e "${GREEN}[ ✔ ] Selected:${RESET} $DEVICE"

VID=$(echo "$DEVICE" | awk '{print $6}' | cut -d':' -f1)
PID=$(echo "$DEVICE" | awk '{print $6}' | cut -d':' -f2)

VID_DEC=$((16#$VID))
PID_DEC=$((16#$PID))

# =======================================
# UPDATE USER CONFIG
# =======================================

sed -i "/^vid=/d" "$CONFIG_FILE"
sed -i "/^pid=/d" "$CONFIG_FILE"

echo "vid=$VID_DEC" >> "$CONFIG_FILE"
echo "pid=$PID_DEC" >> "$CONFIG_FILE"

# =======================================
# UDEV (SAFE)
# =======================================

echo -e "${CYAN}[ + ] Configuring HID access...${RESET}"

GROUP_NAME="linuity"

sudo groupadd "$GROUP_NAME" 2>/dev/null || true
sudo usermod -aG "$GROUP_NAME" "$USER"

RULE_FILE="/etc/udev/rules.d/99-linuity.rules"

echo "SUBSYSTEM==\"hidraw\", ATTRS{idVendor}==\"$VID\", ATTRS{idProduct}==\"$PID\", MODE=\"0660\", GROUP=\"$GROUP_NAME\"" | sudo tee "$RULE_FILE" > /dev/null

sudo udevadm control --reload-rules
sudo udevadm trigger

echo -e "${YELLOW}[ ! ] You may need to re-login${RESET}"

# =======================================
# SYSTEMD SERVICE (ROOT - NECESSARY)
# =======================================

echo -e "${CYAN}[ + ] Installing service...${RESET}"

SERVICE_PATH="/etc/systemd/system/linuity.service"

sudo tee "$SERVICE_PATH" > /dev/null <<EOF
[Unit]
Description=Linuity LED Daemon
After=multi-user.target

[Service]
User=root
WorkingDirectory=$HOME
Environment=HOME=$HOME
ExecStart=$DAEMON_PATH
Restart=always
RestartSec=2

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable linuity.service
sudo systemctl restart linuity.service

# =======================================
# DONE
# =======================================

echo ""
echo "======================================="
echo " Installation Complete"
echo "======================================="
echo ""

echo -e "${CYAN}Logs:${RESET} journalctl -u linuity.service -f"