#!/usr/bin/env bash
set -Eeuo pipefail

# ==============================================================================
# Evidence Processor
#
# File:
#     entrypoint.sh
#
# Purpose:
#     Minimal container startup controller.
#
# Responsibilities:
#     - Prepare /data folder structure.
#     - Seed editable default files.
#     - Normalize UnRAID appdata permissions.
#     - Run startup Python scripts in order.
#
# This script should not:
#     - Parse config.yaml directly.
#     - Create database objects directly.
#     - Process documents directly.
#     - Own detailed application logging.
# ==============================================================================

PUID="${PUID:-99}"
PGID="${PGID:-100}"
UMASK="${UMASK:-0002}"

DATA_DIR="${DATA_DIR:-/data}"
CONFIG_DIR="${CONFIG_DIR:-/data/config}"
LOG_DIR="${LOG_DIR:-/data/logs}"

export EP_CONFIG="${EP_CONFIG:-$CONFIG_DIR/config.yaml}"

mkdir -p "$CONFIG_DIR" "$LOG_DIR"
umask "$UMASK"

# ------------------------------------------------------------------------------
# Seed default files.
#
# Existing user-edited files are never overwritten.
# ------------------------------------------------------------------------------

for file in /app/defaults/*; do
  filename="$(basename "$file")"

  if [ ! -f "$CONFIG_DIR/$filename" ]; then
    cp "$file" "$CONFIG_DIR/$filename"
    echo "[INFO] Seeded default file: $filename"
  fi
done

# ------------------------------------------------------------------------------
# Normalize UnRAID appdata permissions.
# ------------------------------------------------------------------------------

chgrp -R "$PGID" "$DATA_DIR" 2>/dev/null || true
chmod -R g+rwX "$DATA_DIR" 2>/dev/null || true
chmod g+s "$CONFIG_DIR" "$LOG_DIR" 2>/dev/null || true
find "$CONFIG_DIR" -type f -name "*.sh" -exec chmod 775 {} \; 2>/dev/null || true

export USER="${USER:-nobody}"
export LOGNAME="${LOGNAME:-nobody}"
export HOME="${HOME:-/tmp}"

# ------------------------------------------------------------------------------
# Run startup checks.
#
# Detailed logging and exit messages belong inside the Python scripts.
# ------------------------------------------------------------------------------

/app/scripts/check_config.py
/app/scripts/initialize_database.py
exec /app/scripts/check_mariadb.py