#!/bin/bash
# Sayanox‑One Installer — Linux / Termux compatible

echo "[+] Starting Sayanox‑One installation..."

# Check root
if [ "$(id -u)" -ne 0 ]; then
  echo "[!] Run as root/with sudo for full functionality"
fi

# Update system
echo "[+] Updating system packages..."
apt update -y && apt upgrade -y

# Base dependencies
echo "[+] Installing system dependencies..."
apt install -y python3 python3-pip python3-venv git nmap curl wget jq

# Termux extra fix
if [ -d "$PREFIX/termux" ] || [ -n "$TERMUX_VERSION" ]; then
  echo "[+] Applying Termux‑specific fixes..."
  apt install -y libssl-dev libffi-dev build-essential
fi

# Python environment
echo "[+] Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python packages
echo "[+] Installing Python dependencies..."
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# Install CLI link
echo "[+] Registering 'sayanox' command..."
pip install -e .

echo "[✓] Installation complete!"
echo "→ Run: sayanox --target <domain-or-ip> --mode full"
