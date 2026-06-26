#!/bin/bash
set -e

CONFIG_DIR="/data/config"
DEFAULTS_DIR="/app/defaults"

mkdir -p "$CONFIG_DIR"

if [ ! -f "$CONFIG_DIR/config.yaml" ]; then
    echo "[INFO] No config.yaml found. Copying default config..."
    cp "$DEFAULTS_DIR/config.yaml" "$CONFIG_DIR/config.yaml"
fi

if [ ! -f "$CONFIG_DIR/create_db_user.sh" ]; then
    echo "[INFO] No create_db_user.sh found. Copying one-time setup script..."
    cp "$DEFAULTS_DIR/create_db_user.sh" "$CONFIG_DIR/create_db_user.sh"
    chmod +x "$CONFIG_DIR/create_db_user.sh"
fi

mkdir -p /data/logs

echo "[INFO] Evidence Processor starting..."
echo "[INFO] Config: $EP_CONFIG"

exec gosu "${PUID}:${PGID}" python3 /app/scripts/check_mariadb.py