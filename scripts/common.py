#!/usr/bin/env python3
"""
==============================================================================
Evidence Processor

File:
    common.py

Purpose:
    Shared configuration helpers used by all Evidence Processor scripts.

Responsibilities:
    - Load the main YAML configuration file.
    - Read required Docker/runtime environment variables.
    - Normalize MariaDB host and port settings.
    - Provide safe nested configuration lookup.
    - Provide a consistent fail() helper for standalone scripts.

This module should not:
    - Connect to MariaDB.
    - Create database tables.
    - Process documents.
    - Write application logs.

Configuration Design:
    Evidence Processor keeps Docker variables intentionally small.

    Docker / UnRAID provides:
        MARIADB_HOST

    Example:
        MARIADB_HOST=192.168.5.20:3306

    config.yaml provides:
        database.name
        database.username
        database.password
        database.connection_timeout
        database.charset

    This keeps secrets and app-specific settings in the editable config file,
    while Docker only needs to know where MariaDB is located.

Notes:
    - EP_CONFIG may optionally override the config path.
    - If EP_CONFIG is not provided, /app/config/config.yaml is used.
    - For local development, python-dotenv is loaded if a .env file exists,
      but a .env file is not required and should not be committed to GitHub.

==============================================================================
"""

import os
import sys
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv


# ==============================================================================
# Exceptions
# ==============================================================================


class ConfigError(Exception):
    """
    Raised when configuration is missing, invalid, or cannot be loaded.
    """

    pass


# ==============================================================================
# Configuration Loading
# ==============================================================================


def load_config() -> dict:
    """
    Load application configuration from config.yaml and environment variables.

    Source order:
        1. YAML config file
        2. Docker/runtime environment variables

    Required environment variables:
        MARIADB_HOST

    Required YAML values:
        database.name
        database.username
        database.password

    MARIADB_HOST supports:
        192.168.5.20
        192.168.5.20:3306

    If no port is included in MARIADB_HOST, port 3306 is used.

    Returns:
        dict: Unified application configuration.

    Raises:
        ConfigError: If required configuration is missing or invalid.
    """

    # --------------------------------------------------------------------------
    # Optional local .env support
    #
    # This is mainly useful for local development. In UnRAID/Docker, values should
    # be provided as container variables instead. A .env file should not be
    # committed to GitHub.
    # --------------------------------------------------------------------------

    load_dotenv()

    # --------------------------------------------------------------------------
    # Locate config.yaml
    #
    # Normal Docker path:
    #     /app/config/config.yaml
    #
    # Optional override:
    #     EP_CONFIG=/some/other/config.yaml
    # --------------------------------------------------------------------------

    config_path = os.getenv("EP_CONFIG", "/app/config/config.yaml")
    config_file = Path(config_path)

    if not config_file.exists():
        raise ConfigError(f"Config file not found: {config_file}")

    # --------------------------------------------------------------------------
    # Load YAML configuration
    # --------------------------------------------------------------------------

    try:
        with config_file.open("r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}
    except yaml.YAMLError as e:
        raise ConfigError(f"Unable to parse config file: {config_file} :: {e}") from e
    except OSError as e:
        raise ConfigError(f"Unable to read config file: {config_file} :: {e}") from e

    # --------------------------------------------------------------------------
    # Validate database section exists
    # --------------------------------------------------------------------------

    config.setdefault("database", {})

    # --------------------------------------------------------------------------
    # MariaDB Host / Port
    #
    # Docker variable:
    #     MARIADB_HOST=192.168.5.20:3306
    #
    # This keeps the MariaDB network location outside config.yaml, which makes it
    # easy to point the container at a different MariaDB server without editing
    # the mounted config file.
    # --------------------------------------------------------------------------

    mariadb_host_raw = os.getenv("MARIADB_HOST")

    if not mariadb_host_raw:
        raise ConfigError("Missing required environment variable: MARIADB_HOST")

    host, port = parse_host_port(mariadb_host_raw)

    config["database"]["host"] = host
    config["database"]["port"] = port

    # --------------------------------------------------------------------------
    # Required database values from config.yaml
    #
    # These should be edited in:
    #     /mnt/user/appdata/evidence-processor/config/config.yaml
    # --------------------------------------------------------------------------

    required_database_values = [
        "database.name",
        "database.username",
        "database.password",
    ]

    for key in required_database_values:
        value = get_config_value(config, key)

        if value is None or str(value).strip() == "":
            raise ConfigError(f"Missing required config value: {key}")

    # --------------------------------------------------------------------------
    # Optional database defaults
    # --------------------------------------------------------------------------

    config["database"].setdefault("connection_timeout", 10)
    config["database"].setdefault("charset", "utf8mb4")

    return config


# ==============================================================================
# Host / Port Parsing
# ==============================================================================


def parse_host_port(host_value: str) -> tuple[str, int]:
    """
    Parse a host string into hostname and port.

    Supported formats:
        192.168.5.20
        192.168.5.20:3306
        mariadb
        mariadb:3306

    Args:
        host_value:
            Raw host string from MARIADB_HOST.

    Returns:
        tuple[str, int]:
            Hostname and port.

    Raises:
        ConfigError:
            If the host is empty or the port is invalid.
    """

    cleaned = host_value.strip()

    if not cleaned:
        raise ConfigError("MARIADB_HOST is empty")

    if ":" not in cleaned:
        return cleaned, 3306

    host, port_raw = cleaned.rsplit(":", 1)

    host = host.strip()
    port_raw = port_raw.strip()

    if not host:
        raise ConfigError("MARIADB_HOST contains a port but no hostname")

    if not port_raw:
        raise ConfigError("MARIADB_HOST contains ':' but no port number")

    try:
        port = int(port_raw)
    except ValueError:
        raise ConfigError(f"Invalid MariaDB port in MARIADB_HOST: {port_raw}") from None

    if port < 1 or port > 65535:
        raise ConfigError(f"MariaDB port out of valid range: {port}")

    return host, port


# ==============================================================================
# Configuration Lookup
# ==============================================================================


def get_config_value(
    config: dict,
    path: str,
    default: Any = None,
    required: bool = False,
) -> Any:
    """
    Safely read nested configuration values using dot notation.

    Example:
        get_config_value(config, "database.name")
        get_config_value(config, "logging.directory", "/app/logs")

    Args:
        config:
            Configuration dictionary.

        path:
            Dot-separated path to the requested value.

        default:
            Value returned if the path is missing and required=False.

        required:
            If True, missing values raise ConfigError.

    Returns:
        Any:
            Requested configuration value or default.

    Raises:
        ConfigError:
            If required=True and the value is missing.
    """

    current: Any = config

    for part in path.split("."):
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            if required:
                raise ConfigError(f"Missing required config value: {path}")
            return default

    return current


# ==============================================================================
# Script Failure Helper
# ==============================================================================


def fail(message: str, exit_code: int = 1) -> None:
    """
    Print a fatal error and exit.

    This helper is intended for standalone scripts such as:
        check_mariadb.py
        create_schema.py
        load_documents.py

    Args:
        message:
            Error message to display.

        exit_code:
            Process exit code.
    """

    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(exit_code)