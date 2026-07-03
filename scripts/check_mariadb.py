#!/usr/bin/env python3
"""
==============================================================================
Evidence Processor

File:
    check_mariadb.py

Purpose:
    Verify that Evidence Processor can connect to MariaDB.

This script does not:
    - Create databases
    - Create users
    - Create tables
    - Process documents
==============================================================================
"""

from common import ConfigError, fail, load_config
from database import Database, DatabaseError
from logger import get_logger


def main() -> int:
    try:
        config = load_config()
        logger = get_logger("check_mariadb", config)

        logger.info("Starting MariaDB connection check")

        db = Database(config, logger)
        db.connect()

        result = db.query_one("SELECT VERSION() AS version;")

        logger.info("MariaDB connection successful")
        logger.info("Server version: %s", result.get("version"))

        db.disconnect()

        return 0

    except ConfigError as e:
        fail(f"Configuration error: {e}")
        return 1

    except DatabaseError as e:
        fail(f"Database error: {e}")
        return 2

    except Exception as e:
        fail(f"Unexpected error: {e}")
        return 3


if __name__ == "__main__":
    raise SystemExit(main())