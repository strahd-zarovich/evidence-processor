#!/usr/bin/env python3
"""
==============================================================================
Evidence Processor

File:
    create_schema.py

Purpose:
    Create or update the Evidence Processor application schema.

Responsibilities:
    - Connect to the application database.
    - Create application tables.
    - Create indexes.
    - Record the current schema version.

This script is safe to run repeatedly.

This script should not:
    - Create databases.
    - Create users.
    - Process documents.
==============================================================================
"""

from common import ConfigError, load_config
from database import Database, DatabaseError
from logger import get_logger
from schema import CURRENT_SCHEMA_VERSION, create_schema


def main() -> int:
    logger = None

    try:
        config = load_config()
        logger = get_logger("create_schema", config)

        logger.info("Starting schema initialization")
        logger.info("Target schema version: %s", CURRENT_SCHEMA_VERSION)

        db = Database(config, logger)
        db.connect()

        try:
            with db.connection.cursor() as cursor:
                create_schema(cursor)

            db.commit()

        except Exception:
            db.rollback()
            raise

        finally:
            db.disconnect()

        logger.info("Schema initialization complete")

        return 0

    except ConfigError as e:
        if logger:
            logger.error("Configuration error: %s", e)
        else:
            print(f"[ERROR] Configuration error: {e}")
        return 1

    except DatabaseError as e:
        if logger:
            logger.error("Database error: %s", e)
        else:
            print(f"[ERROR] Database error: {e}")
        return 2

    except Exception as e:
        if logger:
            logger.exception("Schema initialization failed")
        else:
            print(f"[ERROR] Schema initialization failed: {e}")
        return 3


if __name__ == "__main__":
    raise SystemExit(main())