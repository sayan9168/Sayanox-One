#!/bin/bash
set -euo pipefail
echo "[+] Setting up Sayanox‑One — Production Mode"

# Require root for full scan capability
if [ "$(id -u)" -ne 0 ]; then
  echo "[!] MUST run as root/sudo — some scans require raw sockets"
  exit 1
fi

apt update -y
apt install -y python3 python3‑pip python3‑venv git nmap dnsutils curl

# Termux specific safe fixes
if [ -n "$TERMUX_VERSION" ]; then
  apt install -y libssl‑dev libffi‑dev build‑essential
  sysctl‑w net.ipv4.tcp_syn_retries=2 2>/dev/null || true
fi

python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
pip install -e .

# Create allowlist if missing
if [ ! -f config/allowlists.txt ]; then
  echo "# ADD YOUR AUTHORIZED TARGETS HERE" > config/allowlists.txt
fi

echo "[✓] Ready — edit allowlists.txt before scanning!"
