#!/usr/bin/env python3
"""
==============================================================================
Evidence Processor

File:
    check_config.py

Purpose:
    Validate the Evidence Processor configuration file before startup continues.

Responsibilities:
    - Confirm config.yaml exists.
    - Confirm config.yaml can be parsed.
    - Confirm required values exist.
    - Confirm database.password has been changed from CHANGE_ME.
    - Confirm basic configuration values are sane.

This script should not:
    - Connect to MariaDB.
    - Create databases.
    - Create users.
    - Create tables.
    - Process documents.

Exit Codes:
    0 = Configuration is valid
    1 = Configuration file missing or unreadable
    2 = Required configuration value missing or invalid
    3 = database.password is still CHANGE_ME
==============================================================================
"""

from common import ConfigError, get_config_value, load_config
from logger import get_logger


REQUIRED_CONFIG_VALUES = [
    "database.host",
    "database.port",
    "database.name",
    "database.username",
    "database.password",
    "database.admin_username",
    "database.admin_password",
    "database.connection_timeout",
    "database.charset",
]


def main() -> int:
    # --------------------------------------------------------------------------
    # Config must be loaded before the normal logger can be created.
    # These prints are intentional and only cover the pre-logger phase.
    # --------------------------------------------------------------------------

    print("[INFO] Checking configuration...")

    try:
        config = load_config()

    except ConfigError as e:
        print(f"[ERROR] Configuration file problem: {e}")
        return 1

    logger = get_logger("check_config", config)

    # --------------------------------------------------------------------------
    # Required values.
    # --------------------------------------------------------------------------

    for key in REQUIRED_CONFIG_VALUES:
        value = get_config_value(config, key)

        if value is None or str(value).strip() == "":
            logger.error("Missing required configuration value: %s", key)
            return 2

    # --------------------------------------------------------------------------
    # Placeholder value checks.
    # --------------------------------------------------------------------------

    db_password = str(get_config_value(config, "database.password", "")).strip()
    admin_password = str(get_config_value(config, "database.admin_password", "")).strip()

    if db_password == "CHANGE_ME":
        logger.error("database.password is still CHANGE_ME")
        logger.error("Edit /data/config/config.yaml before continuing.")
        return 3

    if admin_password == "CHANGE_ME":
        logger.error("database.admin_password is still CHANGE_ME")
        logger.error("Edit /data/config/config.yaml before continuing.")
        return 3

    # --------------------------------------------------------------------------
    # Type / sanity checks.
    # --------------------------------------------------------------------------

    try:
        port = int(get_config_value(config, "database.port"))
    except (TypeError, ValueError):
        logger.error("database.port must be an integer.")
        return 2

    if port < 1 or port > 65535:
        logger.error("database.port must be between 1 and 65535.")
        return 2

    try:
        timeout = int(get_config_value(config, "database.connection_timeout"))
    except (TypeError, ValueError):
        logger.error("database.connection_timeout must be an integer.")
        return 2

    if timeout <= 0:
        logger.error("database.connection_timeout must be greater than zero.")
        return 2

    logger.info("Configuration check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())