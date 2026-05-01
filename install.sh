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
echo " Linuity Installer"
echo "======================================="
echo ""

echo -e "${YELLOW}[ ! ] Warning: This installation may require superuser privileges.${RESET}"
echo ""

cd "$(dirname "$0")"

echo -e "${CYAN}[ + ] Checking pipx...${RESET}"
if ! command -v pipx >/dev/null 2>&1; then
    echo -e "${YELLOW}[ ! ] pipx not found. Installing...${RESET}"
    sudo apt update
    sudo apt install -y pipx
else
    echo -e "${GREEN}[ ✔ ] pipx found${RESET}"
fi
echo ""

echo -e "${CYAN}[ + ] Installing system dependencies...${RESET}"
sudo apt install -y python3-hid
echo -e "${GREEN}[ ✔ ] Dependencies installed${RESET}"
echo ""

echo -e "${CYAN}[ + ] Installing fzf (interactive selector)...${RESET}"
if ! command -v fzf >/dev/null 2>&1; then
    sudo apt install -y fzf
    echo -e "${GREEN}[ ✔ ] fzf installed${RESET}"
else
    echo -e "${GREEN}[ ✔ ] fzf already installed${RESET}"
fi
echo ""

echo -e "${CYAN}[ + ] Ensuring pipx PATH...${RESET}"
pipx ensurepath
echo -e "${GREEN}[ ✔ ] PATH configured${RESET}"
echo ""

echo -e "${CYAN}[ + ] Checking previous installation...${RESET}"
if pipx list | grep -q linuity; then
    echo -e "${YELLOW}[ ! ] Previous installation found. Removing...${RESET}"
    pipx uninstall linuity
    echo -e "${GREEN}[ ✔ ] Removed${RESET}"
else
    echo -e "${GREEN}[ ✔ ] No previous installation found${RESET}"
fi
echo ""

echo -e "${CYAN}[ + ] Installing Linuity via pipx...${RESET}"
pipx install . --system-site-packages --force
pipx runpip linuity install hidapi
echo -e "${GREEN}[ ✔ ] Installation complete${RESET}"
echo ""

echo -e "${CYAN}[ + ] Verifying daemon...${RESET}"
if [ ! -f "$HOME/.local/bin/linuity-daemon" ]; then
    echo -e "${RED}[ x ] Error: linuity-daemon not found!${RESET}"
    exit 1
fi
echo -e "${GREEN}[ ✔ ] Daemon found${RESET}"
echo ""

echo -e "${CYAN}[ + ] Preparing configuration directory...${RESET}"
mkdir -p "$HOME/.config/linuity"

if [ ! -f "$HOME/.config/linuity/preset.conf" ]; then
    cp linuity/resources/preset.conf.example "$HOME/.config/linuity/preset.conf"
    echo -e "${GREEN}[ ✔ ] Default preset created${RESET}"
else
    echo -e "${GREEN}[ ✔ ] Preset already exists${RESET}"
fi
echo ""

echo -e "${CYAN}[ + ] Installing systemd service...${RESET}"

SERVICE_PATH="/etc/systemd/system/linuity.service"
DAEMON_PATH="$HOME/.local/bin/linuity-daemon"

cat <<EOF | sudo tee "$SERVICE_PATH" > /dev/null
[Unit]
Description=Linuity LED Daemon
After=multi-user.target systemd-udev-settle.service
Wants=systemd-udev-settle.service

[Service]
ExecStart=$DAEMON_PATH
Restart=always
RestartSec=2

StandardOutput=journal
StandardError=journal

StartLimitIntervalSec=0

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable linuity.service

echo -e "${GREEN}[ ✔ ] Service installed${RESET}"

# =======================================
# DEVICE SELECTION (FZF)
# =======================================

echo -e "${CYAN}[ + ] Detecting USB devices...${RESET}"
echo ""

echo -e "${YELLOW}[ ! ] IMPORTANT:${RESET}"
echo -e "${YELLOW}[ ! ] Select the device that contains:${RESET} ${GREEN}Controller${RESET}"
echo ""
echo -e "${YELLOW}[ ! ] Example:${RESET}"
echo -e "      ${GREEN}HyperX QuadCast 2 Controller${RESET}"
echo ""
echo -e "${RED}[ x ] Do NOT select:${RESET} HyperX QuadCast 2 (audio device)"
echo ""

DEVICE=$(lsusb | fzf --prompt="Select device > " --height=15 --border)

if [ -z "$DEVICE" ]; then
    echo -e "${RED}[ x ] No device selected${RESET}"
    exit 1
fi

echo ""
echo -e "${GREEN}[ ✔ ] Selected:${RESET} $DEVICE"

if ! echo "$DEVICE" | grep -qi "controller"; then
    echo ""
    echo -e "${RED}[ x ] Warning: Selected device does NOT look like a controller${RESET}"
    echo -e "${YELLOW}[ ! ] This may cause the daemon to fail${RESET}"
    echo ""

    # shellcheck disable=SC2162
    read -p "$(echo -e "${CYAN}[ + ] Continue anyway? (y/N): ${RESET}")" CONFIRM
    if [[ ! "$CONFIRM" =~ ^[Yy]$ ]]; then
        echo -e "${RED}[ x ] Installation aborted${RESET}"
        exit 1
    fi
fi

VID=$(echo "$DEVICE" | awk '{print $6}' | cut -d':' -f1)
PID=$(echo "$DEVICE" | awk '{print $6}' | cut -d':' -f2)

echo ""
echo -e "${GREEN}[ ✔ ] VID: $VID${RESET}"
echo -e "${GREEN}[ ✔ ] PID: $PID${RESET}"
echo ""

echo -e "${CYAN}[ + ] Converting values...${RESET}"
VID_DEC=$((16#$VID))
PID_DEC=$((16#$PID))

VID_PADDED=$(printf "%08X" 0x"$VID")
PID_PADDED=$(printf "%08X" 0x"$PID")

echo -e "${GREEN}[ ✔ ] VID (decimal): $VID_DEC${RESET}"
echo -e "${GREEN}[ ✔ ] PID (decimal): $PID_DEC${RESET}"
echo ""

# =======================================
# UPDATE CONFIG
# =======================================

CONFIG_FILE="$HOME/.config/linuity/preset.conf"

echo -e "${CYAN}[ + ] Updating preset configuration...${RESET}"

if [ ! -f "$CONFIG_FILE" ]; then
    echo -e "${RED}[ x ] preset.conf not found!${RESET}"
    exit 1
fi

if grep -q "^vid=" "$CONFIG_FILE"; then
    sed -i "s/^vid=.*/vid=$VID_DEC/" "$CONFIG_FILE"
else
    echo "vid=$VID_DEC" >> "$CONFIG_FILE"
fi

if grep -q "^pid=" "$CONFIG_FILE"; then
    sed -i "s/^pid=.*/pid=$PID_DEC/" "$CONFIG_FILE"
else
    echo "pid=$PID_DEC" >> "$CONFIG_FILE"
fi

echo -e "${GREEN}[ ✔ ] Configuration updated${RESET}"
echo ""

# =======================================
# UDEV
# =======================================

echo -e "${CYAN}[ + ] Configuring HID permissions...${RESET}"
echo 'KERNEL=="hidraw*", SUBSYSTEM=="hidraw", MODE="0666"' | sudo tee /etc/udev/rules.d/99-hidraw-permissions.rules > /dev/null
echo -e "${GREEN}[ ✔ ] Permissions configured${RESET}"
echo ""

echo -e "${CYAN}[ + ] Configuring auto-restart on device reconnect...${RESET}"

RULE_FILE="/etc/udev/rules.d/98-linuity-restart.rules"

echo "ACTION==\"bind\", SUBSYSTEM==\"hid\", ENV{HID_ID}==\"0003:${VID_PADDED}:${PID_PADDED}\", RUN+=\"/bin/sh -c '/usr/bin/systemctl restart linuity.service'\"" | sudo tee "$RULE_FILE" > /dev/null

echo -e "${GREEN}[ ✔ ] Udev rule created${RESET}"
echo ""

echo -e "${CYAN}[ + ] Reloading udev rules...${RESET}"
sudo udevadm control --reload-rules
sudo udevadm trigger
echo -e "${GREEN}[ ✔ ] Udev reloaded${RESET}"
echo ""

# =======================================
# START SERVICE
# =======================================

echo -e "${CYAN}[ + ] Starting service...${RESET}"
sudo systemctl restart linuity.service

if sudo systemctl is-active --quiet linuity.service; then
    echo -e "${GREEN}[ ✔ ] Service is running${RESET}"
else
    echo -e "${RED}[ x ] Service failed to start${RESET}"
    echo "      Run: sudo systemctl status linuity.service"
fi

echo ""
echo "======================================="
echo " Installation Complete"
echo "======================================="
echo ""
echo -e "${CYAN}[ + ] You can now run:${RESET}"
echo "      linuity --mode blinking --save"
echo ""
echo -e "${CYAN}[ + ] View logs with:${RESET}"
echo "      journalctl -u linuity.service -f"
echo ""