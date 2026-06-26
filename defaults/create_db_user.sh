#!/bin/bash
# ==============================================================================
# Evidence Processor
#
# File:
#     create_db_user.sh
#
# Purpose:
#     One-time MariaDB initialization script.
#
# Description:
#     This script creates the Evidence Processor database and the
#     application user account required by Evidence Processor.
#
#     After successful execution, this script may be deleted.
#
# Requirements:
#     • MariaDB server running
#     • Root or administrator credentials
#     • MARIADB_HOST configured in Docker
#
# ==============================================================================

set -Eeuo pipefail

# ------------------------------------------------------------------------------
# Administrator Credentials
#
# Enter your MariaDB administrator credentials below.
# These credentials are ONLY used while running this script.
# ------------------------------------------------------------------------------

ADMIN_USER="root"
ADMIN_PASSWORD="CHANGE_ME"

# ------------------------------------------------------------------------------
# Read Configuration
# ------------------------------------------------------------------------------

CONFIG_FILE="${EP_CONFIG:-/data/config/config.yaml}"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "ERROR: Configuration file not found: $CONFIG_FILE"
    exit 1
fi

if [ -z "${MARIADB_HOST:-}" ]; then
    echo "ERROR: MARIADB_HOST is not set."
    exit 1
fi

DB_HOST="$(echo "$MARIADB_HOST" | cut -d':' -f1)"
DB_PORT="$(echo "$MARIADB_HOST" | cut -s -d':' -f2)"

if [ -z "$DB_PORT" ]; then
    DB_PORT="3306"
fi

DB_NAME="$(python3 /app/scripts/read_config.py database.name)"
EP_USER="$(python3 /app/scripts/read_config.py database.username)"
EP_PASSWORD="$(python3 /app/scripts/read_config.py database.password)"

if [ "$EP_PASSWORD" = "CHANGE_ME" ]; then
    echo "ERROR: database.password is still CHANGE_ME in config.yaml"
    exit 1
fi

echo "=============================================================="
echo "Evidence Processor Database Setup"
echo "=============================================================="
echo "Server   : $DB_HOST:$DB_PORT"
echo "Database : $DB_NAME"
echo "User     : $EP_USER"
echo ""

mysql \
    -h "$DB_HOST" \
    -P "$DB_PORT" \
    -u "$ADMIN_USER" \
    -p"$ADMIN_PASSWORD" <<EOF

CREATE DATABASE IF NOT EXISTS \`$DB_NAME\`;

CREATE USER IF NOT EXISTS '$EP_USER'@'%' IDENTIFIED BY '$EP_PASSWORD';

GRANT ALL PRIVILEGES ON \`$DB_NAME\`.* TO '$EP_USER'@'%';

FLUSH PRIVILEGES;

EOF

echo ""
echo "Database setup complete."