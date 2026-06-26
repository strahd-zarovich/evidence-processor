#!/usr/bin/env python3
"""
==============================================================================
Evidence Processor

File:
    read_config.py

Purpose:
    Read a single configuration value from config.yaml.

Usage:
    python3 read_config.py database.name
    python3 read_config.py database.username

Returns:
    The requested configuration value.

Exit Codes:
    0 = Success
    1 = Error

==============================================================================
"""

import sys

from common import get_config_value, load_config


def main():

    if len(sys.argv) != 2:
        print("Usage: read_config.py <config.path>", file=sys.stderr)
        sys.exit(1)

    config = load_config()

    value = get_config_value(
        config,
        sys.argv[1],
        required=True
    )

    print(value)


if __name__ == "__main__":
    main()