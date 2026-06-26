import logging
from pathlib import Path

from common import get_config_value


def get_logger(name: str, config: dict) -> logging.Logger:
    """
    Create a consistent logger for all Evidence Processor scripts.
    """

    log_level_name = get_config_value(config, "application.log_level", "INFO")
    log_level = getattr(logging, log_level_name.upper(), logging.INFO)

    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # Prevent duplicate handlers if imported more than once
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_enabled = get_config_value(config, "logging.console", True)
    if console_enabled:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    file_enabled = get_config_value(config, "logging.file", True)
    if file_enabled:
        log_dir = Path(get_config_value(config, "logging.directory", "/app/logs"))
        log_dir.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(
            log_dir / "evidence_processor.log",
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger