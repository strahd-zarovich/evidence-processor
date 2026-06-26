#!/usr/bin/env bash
set -Eeuo pipefail

# ------------------------------------------------------------------------------
# Evidence Processor Entrypoint
#
# Responsibilities:
#   - Prepare /data folder structure.
#   - Seed editable config files from /app/defaults.
#   - Normalize permissions for UnRAID appdata.
#   - Run the current startup command.
# ------------------------------------------------------------------------------

PUID="${PUID:-99}"
PGID="${PGID:-100}"
UMASK="${UMASK:-0002}"

DATA_DIR="${DATA_DIR:-/data}"
CONFIG_DIR="${CONFIG_DIR:-/data/config}"
LOG_DIR="${LOG_DIR:-/data/logs}"

export EP_CONFIG="${EP_CONFIG:-$CONFIG_DIR/config.yaml}"

log() {
  local level="${1:-INFO}"
  shift || true
  echo "[$level] $*"
}

mkdir -p "$CONFIG_DIR" "$LOG_DIR"
umask "$UMASK"

# ------------------------------------------------------------------------------
# Seed default config files if missing.
# Existing user-edited files are never overwritten.
# ------------------------------------------------------------------------------

for file in /app/defaults/*; do
  filename="$(basename "$file")"

  if [ ! -f "$CONFIG_DIR/$filename" ]; then
    cp "$file" "$CONFIG_DIR/$filename"
    log INFO "Seeded default config: $filename"
  fi
done

# ------------------------------------------------------------------------------
# Normalize permissions so UnRAID SMB/editor can modify config files.
# ------------------------------------------------------------------------------

chgrp -R "$PGID" "$DATA_DIR" 2>/dev/null || true
chmod -R g+rwX "$DATA_DIR" 2>/dev/null || true
chmod g+s "$CONFIG_DIR" "$LOG_DIR" 2>/dev/null || true

# Also make shell scripts executable.
find "$CONFIG_DIR" -type f -name "*.sh" -exec chmod 775 {} \; 2>/dev/null || true

# Avoid getpass/getuser issues when running as numeric UID.
export USER="${USER:-nobody}"
export LOGNAME="${LOGNAME:-nobody}"
export HOME="${HOME:-/tmp}"

log INFO "Evidence Processor starting..."
log INFO "Config: $EP_CONFIG"
log INFO "MariaDB Host: ${MARIADB_HOST:-not set}"

# For v0.0.1, run the MariaDB connection check.
exec python3 /app/scripts/check_mariadb.py