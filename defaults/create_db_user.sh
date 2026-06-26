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

set -e

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

CONFIG_FILE="/app/config/config.yaml"

if [ ! -f "$CONFIG_FILE" ]; then
    echo ""
    echo "ERROR: Configuration file not found."
    echo ""
    echo "Expected:"
    echo "    $CONFIG_FILE"
    echo ""
    exit 1
fi

# ------------------------------------------------------------------------------
# Read MariaDB Host
# ------------------------------------------------------------------------------

if [ -z "$MARIADB_HOST" ]; then
    echo ""
    echo "ERROR: Docker variable MARIADB_HOST is not set."
    echo ""
    exit 1
fi

DB_HOST=$(echo "$MARIADB_HOST" | cut -d':' -f1)
DB_PORT=$(echo "$MARIADB_HOST" | cut -d':' -f2)

if [ "$DB_PORT" = "$DB_HOST" ]; then
    DB_PORT=3306
fi

# ------------------------------------------------------------------------------
# Read Database Information from config.yaml
# ------------------------------------------------------------------------------

DB_NAME=$(grep "name:" "$CONFIG_FILE" | head -1 | awk '{print $2}')
EP_USER=$(grep "username:" "$CONFIG_FILE" | head -1 | awk '{print $2}')
EP_PASSWORD=$(grep "password:" "$CONFIG_FILE" | head -1 | awk '{print $2}')

echo ""
echo "=============================================================="
echo " Evidence Processor Database Setup"
echo "=============================================================="
echo ""
echo "Server:"
echo "    $DB_HOST:$DB_PORT"
echo ""
echo "Database:"
echo "    $DB_NAME"
echo ""
echo "Application User:"
echo "    $EP_USER"
echo ""

read -p "Continue (y/N)? " answer

if [[ ! "$answer" =~ ^[Yy]$ ]]; then
    echo ""
    echo "Cancelled."
    exit 0
fi

echo ""
echo "Creating database and user..."
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
echo "=============================================================="
echo " Setup Complete"
echo "=============================================================="
echo ""
echo "Database successfully created."
echo "Application user successfully created."
echo ""
echo "You may now delete this script if desired."
echo ""