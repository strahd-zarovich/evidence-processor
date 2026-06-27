#!/usr/bin/env bash
set -Eeuo pipefail

# ==============================================================================
# Evidence Processor
#
# File:
#     entrypoint.sh
#
# Purpose:
#     Container startup controller.
#
# Responsibilities:
#     - Prepare /data folder structure.
#     - Seed editable config files from /app/defaults.
#     - Normalize UnRAID appdata permissions.
#     - Run startup checks in order.
#     - Stop with clear messages when setup is incomplete.
#
# This script should not:
#     - Parse config.yaml directly.
#     - Create database objects directly.
#     - Process documents directly.
# ==============================================================================

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
# Seed default files.
#
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
# Normalize UnRAID appdata permissions.
# ------------------------------------------------------------------------------

chgrp -R "$PGID" "$DATA_DIR" 2>/dev/null || true
chmod -R g+rwX "$DATA_DIR" 2>/dev/null || true
chmod g+s "$CONFIG_DIR" "$LOG_DIR" 2>/dev/null || true
find "$CONFIG_DIR" -type f -name "*.sh" -exec chmod 775 {} \; 2>/dev/null || true

export USER="${USER:-nobody}"
export LOGNAME="${LOGNAME:-nobody}"
export HOME="${HOME:-/tmp}"

log INFO "Evidence Processor starting..."
log INFO "Config: $EP_CONFIG"
log INFO "MariaDB Host: ${MARIADB_HOST:-not set}"

# ------------------------------------------------------------------------------
# Step 1: Validate config.yaml.
# ------------------------------------------------------------------------------

set +e
/app/scripts/check_config.py
CONFIG_RC=$?
set -e

case "$CONFIG_RC" in
  0)
    log INFO "Configuration check passed."
    ;;
  3)
    log ERROR "Database password is still CHANGE_ME."
    log ERROR "Edit /data/config/config.yaml, then restart the container."
    exit 1
    ;;
  *)
    log ERROR "Configuration check failed with exit code $CONFIG_RC."
    exit 1
    ;;
esac

# ------------------------------------------------------------------------------
# Step 2: Check whether configured database already exists.
# ------------------------------------------------------------------------------

# set +e
# /app/scripts/check_database.py
# DB_CHECK_RC=$?
# set -e

# case "$DB_CHECK_RC" in
#   0)
#     log INFO "Database already exists. Continuing startup."
#     ;;
#   1)
#     log WARNING "Database does not exist yet."
#     log INFO "Database initialization will be added in the next build."
#     exit 1
#     ;;
#   *)
#     log ERROR "Database check failed. Verify MariaDB host, port, and configuration."
#     exit 1
#     ;;
# esac

# ------------------------------------------------------------------------------
# Step 3: Ensure MariaDB database and application user exist.
# ------------------------------------------------------------------------------

/app/scripts/initialize_database.py

# ------------------------------------------------------------------------------
# Step 4: Final MariaDB connection test using the application user.
# ------------------------------------------------------------------------------

exec /app/scripts/check_mariadb.py