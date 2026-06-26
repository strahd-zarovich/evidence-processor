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


REQUIRED_CONFIG_VALUES = [
    "database.name",
    "database.username",
    "database.password",
    "database.connection_timeout",
    "database.charset",
]


def main() -> int:
    try:
        config = load_config()

    except ConfigError as e:
        print(f"CONFIG ERROR: {e}")
        return 1

    for key in REQUIRED_CONFIG_VALUES:
        value = get_config_value(config, key)

        if value is None or str(value).strip() == "":
            print(f"CONFIG ERROR: Missing required value: {key}")
            return 2

    db_password = str(get_config_value(config, "database.password", "")).strip()

    if db_password == "CHANGE_ME":
        print("CONFIG ERROR: database.password is still CHANGE_ME")
        print("Edit /data/config/config.yaml before continuing.")
        return 3

    print("Configuration check successful.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())