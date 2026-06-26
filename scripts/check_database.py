#!/usr/bin/env python3
"""
==============================================================================
Evidence Processor

File:
    check_database.py

Purpose:
    Check whether the configured Evidence Processor database exists.

Exit Codes:
    0 = Database exists
    1 = Database does not exist
    2 = Configuration or connection error
==============================================================================
"""

from common import ConfigError, get_config_value, load_config
from database import Database, DatabaseError
from logger import get_logger


def main():
    try:
        config = load_config()
        logger = get_logger("check_database", config)

        db_name = get_config_value(config, "database.name", required=True)

        logger.info("Checking for database: %s", db_name)

        db = Database(config, logger)
        db.connect()

        result = db.query_one(
            """
            SELECT SCHEMA_NAME
            FROM INFORMATION_SCHEMA.SCHEMATA
            WHERE SCHEMA_NAME = %s;
            """,
            (db_name,),
        )

        db.disconnect()

        if result:
            logger.info("Database exists: %s", db_name)
            print(f"Database exists: {db_name}")
            return 0

        logger.warning("Database does not exist: %s", db_name)
        print(f"Database does not exist: {db_name}")
        return 1

    except (ConfigError, DatabaseError) as e:
        print(f"ERROR: {e}")
        return 2

    except Exception as e:
        print(f"ERROR: Unexpected error: {e}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())