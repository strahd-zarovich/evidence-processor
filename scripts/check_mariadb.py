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


def main():
    try:
        config = load_config()
        logger = get_logger("check_mariadb", config)

        logger.info("Starting MariaDB connection check")

        db = Database(config, logger)
        db.connect()
        db.ping()

        result = db.query_one(
            "SELECT VERSION() AS version;"
        )

        db.disconnect()

        logger.info("MariaDB connection successful")
        logger.info("Server version: %s", result.get("version"))

        print("MariaDB connection successful.")
        print(f"Server version: {result.get('version')}")

    except ConfigError as e:
        fail(f"Configuration error: {e}")

    except DatabaseError as e:
        fail(f"Database error: {e}")

    except Exception as e:
        fail(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()