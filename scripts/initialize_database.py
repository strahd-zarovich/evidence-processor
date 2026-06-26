#!/usr/bin/env python3
"""
==============================================================================
Evidence Processor

File:
    initialize_database.py

Purpose:
    Ensure the Evidence Processor MariaDB database and application user exist.

Responsibilities:
    - Connect to MariaDB using administrator credentials.
    - Create the configured database if missing.
    - Create the configured application user if missing.
    - Grant permissions on the configured database.
    - Exit cleanly if everything already exists.

This script is safe to run repeatedly.

This script should not:
    - Process documents.
    - Create application tables.
    - Build timelines.
==============================================================================
"""

import pymysql

from common import ConfigError, get_config_value, load_config
from logger import get_logger


def main() -> int:
    try:
        config = load_config()
        logger = get_logger("initialize_database", config)

        host = get_config_value(config, "database.host", required=True)
        port = int(get_config_value(config, "database.port", 3306))
        db_name = get_config_value(config, "database.name", required=True)
        app_user = get_config_value(config, "database.username", required=True)
        app_password = get_config_value(config, "database.password", required=True)

        admin_user = get_config_value(config, "database.admin_username", required=True)
        admin_password = get_config_value(config, "database.admin_password", required=True)

        logger.info("Starting database initialization")
        logger.info("MariaDB host: %s:%s", host, port)
        logger.info("Database: %s", db_name)
        logger.info("Application user: %s", app_user)

        connection = pymysql.connect(
            host=host,
            port=port,
            user=admin_user,
            password=admin_password,
            charset=get_config_value(config, "database.charset", "utf8mb4"),
            connect_timeout=int(get_config_value(config, "database.connection_timeout", 10)),
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True,
        )

        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`;")

            cursor.execute(
                "SELECT User, Host FROM mysql.user WHERE User = %s AND Host = %s;",
                (app_user, "%"),
            )
            user_exists = cursor.fetchone()

            if not user_exists:
                cursor.execute(
                    f"CREATE USER %s@'%%' IDENTIFIED BY %s;",
                    (app_user, app_password),
                )
                logger.info("Created application user: %s", app_user)
            else:
                logger.info("Application user already exists: %s", app_user)

            cursor.execute(
                f"GRANT ALL PRIVILEGES ON `{db_name}`.* TO %s@'%%';",
                (app_user,),
            )

            cursor.execute("FLUSH PRIVILEGES;")

        connection.close()

        logger.info("Database initialization complete")
        print("Database initialization complete.")
        return 0

    except ConfigError as e:
        print(f"CONFIG ERROR: {e}")
        return 1

    except Exception as e:
        print(f"ERROR: Database initialization failed: {e}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())