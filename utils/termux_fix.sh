#!/bin/bash
# Fix Termux low‑memory/permission issues
if [ -n "$TERMUX_VERSION" ]; then
    echo "[*] Applying Termux optimizations"
    sysctl -w net.ipv4.tcp_syn_retries=2 2>/dev/null
    ulimit -n 4096
fi
