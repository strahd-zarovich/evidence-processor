import os
import sys
from pathlib import Path

import yaml
from dotenv import load_dotenv


class ConfigError(Exception):
    pass


def load_config():
    """
    Load application config from YAML and environment variables.
    YAML holds defaults.
    Environment variables hold machine-specific settings and secrets.
    """

    load_dotenv()

    config_path = os.getenv("EP_CONFIG", "/app/defaults/config.yaml")
    config_file = Path(config_path)

    if not config_file.exists():
        raise ConfigError(f"Config file not found: {config_file}")

    with config_file.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f) or {}

    mariadb_host_raw = os.getenv("MARIADB_HOST")
    mariadb_password = os.getenv("MARIADB_PASSWORD")

    if not mariadb_host_raw:
        raise ConfigError("Missing required environment variable: MARIADB_HOST")

    if not mariadb_password:
        raise ConfigError("Missing required environment variable: MARIADB_PASSWORD")

    config.setdefault("database", {})

    # Allow MARIADB_HOST to be either:
    #   192.168.15.20
    #   192.168.15.20:3307
    if ":" in mariadb_host_raw:
        host, port_raw = mariadb_host_raw.rsplit(":", 1)

        if not host.strip():
            raise ConfigError("MARIADB_HOST contains a port but no host")

        try:
            port = int(port_raw)
        except ValueError:
            raise ConfigError(f"Invalid MariaDB port in MARIADB_HOST: {port_raw}")

        config["database"]["host"] = host.strip()
        config["database"]["port"] = port
    else:
        config["database"]["host"] = mariadb_host_raw.strip()
        config["database"].setdefault("port", 3306)

    config["database"]["password"] = mariadb_password

    return config


def get_config_value(config, path, default=None, required=False):
    """
    Safely read nested config values using dot notation.

    Example:
        get_config_value(config, "database.port")
    """

    current = config

    for part in path.split("."):
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            if required:
                raise ConfigError(f"Missing required config value: {path}")
            return default

    return current


def fail(message, exit_code=1):
    """
    Print a fatal error and exit.
    Used by standalone scripts.
    """

    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(exit_code)